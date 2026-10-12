"""
Laptop & Windows Automation Controller
Allows Jia to control Zain Sultan's laptop: applications, wallpapers, system stats.
"""

import os
import sys
import subprocess
import shutil
import ctypes
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional

class LaptopController:
    """Manages local Windows operations for Boss Zain Sultan."""

    WALLPAPERS_DIR = Path("wallpapers").resolve()

    # Curated high-res aesthetic wallpapers for Boss Zain
    WALLPAPER_PRESETS = {
        "cyber": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=85",
        "neon": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1920&q=85",
        "nature": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920&q=85",
        "space": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1920&q=85",
        "dark": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1920&q=85",
        "aesthetic": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=85"
    }

    @classmethod
    def get_chrome_path(cls) -> Optional[str]:
        """Checks for Google Chrome executable in standard locations."""
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            shutil.which("chrome"),
            shutil.which("chrome.exe")
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return None

    @classmethod
    def get_edge_path(cls) -> Optional[str]:
        """Checks for Microsoft Edge executable."""
        candidates = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            shutil.which("msedge"),
            shutil.which("msedge.exe")
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return None

    @classmethod
    def open_browser(cls, target_browser: str = "chrome", url: Optional[str] = None) -> Dict[str, Any]:
        """
        Attempts to open requested browser. If Chrome is requested but missing,
        notifies Boss Zain that Chrome is absent and Edge is available.
        """
        target_browser = target_browser.lower()
        chrome_exe = cls.get_chrome_path()
        edge_exe = cls.get_edge_path()

        if "chrome" in target_browser:
            if chrome_exe:
                args = [chrome_exe]
                if url:
                    args.append(url)
                subprocess.Popen(args)
                return {"success": True, "browser": "Chrome", "message": "Google Chrome open kar diya hai, Boss Zain!"}
            else:
                # Chrome is not installed on the laptop!
                return {
                    "success": False,
                    "browser": "Chrome",
                    "not_found": True,
                    "fallback_available": bool(edge_exe),
                    "fallback_name": "Microsoft Edge",
                    "message": "Boss Zain, aapke laptop mein Google Chrome install nahi mila. Lekin Microsoft Edge available hai! Kya main Edge open kar doon?"
                }
        
        elif "edge" in target_browser:
            if edge_exe:
                args = [edge_exe]
                if url:
                    args.append(url)
                subprocess.Popen(args)
                return {"success": True, "browser": "Microsoft Edge", "message": "Microsoft Edge open kar diya hai, Boss Zain!"}
            else:
                return {"success": False, "browser": "Edge", "message": "Microsoft Edge bhi nahi mila."}
        
        else:
            # Open default browser
            import webbrowser
            webbrowser.open(url or "https://www.google.com")
            return {"success": True, "browser": "Default", "message": "Browser open kar diya hai, Boss!"}

    @classmethod
    def open_system_app(cls, app_name: str) -> Dict[str, Any]:
        """Opens standard Windows applications by name."""
        app_name = app_name.lower().strip()
        app_map = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "calc": ["calc.exe"],
            "explorer": ["explorer.exe"],
            "files": ["explorer.exe"],
            "cmd": ["cmd.exe"],
            "terminal": ["powershell.exe"],
            "powershell": ["powershell.exe"],
            "settings": ["start", "ms-settings:"],
            "task manager": ["taskmgr.exe"],
            "taskmgr": ["taskmgr.exe"],
            "code": ["code.cmd"],
            "vs code": ["code.cmd"],
            "vscode": ["code.cmd"]
        }

        # Handle browser specifically
        if "chrome" in app_name:
            return cls.open_browser("chrome")
        elif "edge" in app_name:
            return cls.open_browser("edge")

        for key, cmd in app_map.items():
            if key in app_name:
                try:
                    if len(cmd) == 2 and cmd[0] == "start":
                        os.system(f"{cmd[0]} {cmd[1]}")
                    else:
                        subprocess.Popen(cmd, shell=True)
                    return {"success": True, "app": key, "message": f"{key.title()} open kar diya hai, Boss Zain!"}
                except Exception as e:
                    return {"success": False, "error": str(e)}

        # Try generic shell open
        try:
            subprocess.Popen(app_name, shell=True)
            return {"success": True, "app": app_name, "message": f"'{app_name}' run kar diya hai, Boss."}
        except Exception as e:
            return {"success": False, "error": str(e), "message": f"'{app_name}' open karne mein error aaya: {e}"}

    @classmethod
    def change_wallpaper(cls, theme: str = "cyber") -> Dict[str, Any]:
        """
        Downloads a wallpaper matching the theme and sets it as the Windows desktop wallpaper.
        """
        cls.WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)
        theme_key = "cyber"
        for k in cls.WALLPAPER_PRESETS.keys():
            if k in theme.lower():
                theme_key = k
                break

        url = cls.WALLPAPER_PRESETS.get(theme_key, cls.WALLPAPER_PRESETS["cyber"])
        file_path = cls.WALLPAPERS_DIR / f"wallpaper_{theme_key}.jpg"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                with open(file_path, "wb") as f:
                    f.write(resp.read())

            # Apply Windows Wallpaper via ctypes (SPI_SETDESKWALLPAPER = 20)
            abs_path = str(file_path.resolve())
            SPI_SETDESKWALLPAPER = 20
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDWININICHANGE = 0x02
            flags = SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
            result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, flags)

            if result:
                return {
                    "success": True,
                    "theme": theme_key,
                    "path": abs_path,
                    "message": f"Zain Boss! Maine aapka desktop wallpaper change kar ke stylish '{theme_key.title()}' theme laga diya hai. Kaisa lag raha hai?"
                }
            else:
                return {"success": False, "message": "Wallpaper apply karne mein issue aaya."}
        except Exception as e:
            return {"success": False, "error": str(e), "message": f"Wallpaper download nahi ho saka: {str(e)}"}

    @classmethod
    def get_system_telemetry(cls) -> Dict[str, Any]:
        """Gathers system stats for Boss Zain."""
        import platform
        return {
            "os": platform.system() + " " + platform.release(),
            "computer_name": platform.node(),
            "time": time.strftime("%I:%M %p"),
            "date": time.strftime("%A, %d %B %Y"),
            "boss": "Zain Sultan",
            "chrome_installed": bool(cls.get_chrome_path()),
            "edge_installed": bool(cls.get_edge_path())
        }
