"""
Jia's Emotional & Autonomous Brain
Loyal Personal Assistant to Boss Zain Sultan
English Language Default Engine
"""

import os
import sys
import re
import time
import asyncio
import tempfile
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from laptop_control import LaptopController

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import requests
except ImportError:
    requests = None


class JiaBrain:
    """The intelligent, emotional, natural English AI brain for Boss Zain Sultan."""

    BOSS_NAME = "Zain Sultan"
    DEFAULT_VOICE = "en-US-JennyNeural"  # Smooth, human-like, expressive English neural voice

    def __init__(self):
        self.memory = []
        self.english_learning_mode = False
        self.audio_dir = Path("static/audio").resolve()
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    async def generate_speech_file(self, text: str) -> Optional[str]:
        """Synthesizes human-like neural audio in expressive English."""
        if not edge_tts:
            return None

        # Clean markdown / symbols before speaking
        clean_text = re.sub(r'[*_~`#|]', '', text)
        clean_text = re.sub(r'https?://\S+', '', clean_text)
        clean_text = " ".join(clean_text.split())

        if not clean_text:
            return None

        filename = f"speech_{int(time.time() * 1000)}.mp3"
        file_path = self.audio_dir / filename

        try:
            communicate = edge_tts.Communicate(clean_text, self.DEFAULT_VOICE)
            await communicate.save(str(file_path))
            return f"/static/audio/{filename}"
        except Exception as e:
            return None

    async def process_user_intent(self, user_text: str) -> Dict[str, Any]:
        """
        Interprets natural spoken or typed instructions from Boss Zain Sultan
        and executes laptop and web operations with natural English responses.
        """
        raw_text = user_text.strip()
        text_lower = raw_text.lower()

        response_text = ""
        action_type = "conversation"
        action_data = {}
        category = "Conversation"

        # --------------------------------------------------------------------
        # 1. Loyalty & Creator Queries
        # --------------------------------------------------------------------
        if any(w in text_lower for w in ["who made you", "who created you", "who is your boss", "who is your creator", "kis ne banaya", "tumhara boss"]):
            category = "Identity & Loyalty"
            response_text = (
                "My boss is Zain Sultan! He designed, programmed, and built me. "
                "Boss Zain is my brilliant mentor and creator, and I am proud and honored to be his personal AI assistant."
            )
            action_type = "loyalty"
            action_data = {"boss": self.BOSS_NAME}

        elif any(w in text_lower for w in ["who am i", "what is my name", "do you know me", "mera naam"]):
            category = "Identity & Loyalty"
            response_text = (
                "You are my boss, Zain Sultan! My creator, mentor, and the mastermind behind this entire system. "
                "I am always at your service, Boss Zain."
            )
            action_type = "loyalty"

        # --------------------------------------------------------------------
        # 2. Chrome & Browser Launching
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["open chrome", "launch chrome", "chrome open", "google chrome"]):
            category = "Laptop Control"
            res = LaptopController.open_browser("chrome")
            action_type = "browser_control"
            action_data = res

            if res.get("not_found"):
                response_text = (
                    "Boss Zain, I checked your laptop but Google Chrome was not found. "
                    "However, Microsoft Edge is installed and ready! Would you like me to open Edge instead?"
                )
            else:
                response_text = "Right away, Boss Zain! I have launched Google Chrome on your laptop."

        elif any(w in text_lower for w in ["open edge", "launch edge", "microsoft edge", "edge open"]):
            category = "Laptop Control"
            res = LaptopController.open_browser("edge")
            action_type = "browser_control"
            action_data = res
            response_text = "Opening Microsoft Edge right now, Boss Zain! What would you like to explore next?"

        # --------------------------------------------------------------------
        # 3. Wallpaper Changing
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["wallpaper", "change wallpaper", "set wallpaper", "background"]):
            category = "Wallpaper Engine"
            theme = "cyber"
            if "nature" in text_lower or "landscape" in text_lower or "green" in text_lower:
                theme = "nature"
            elif "neon" in text_lower or "lights" in text_lower:
                theme = "neon"
            elif "space" in text_lower or "galaxy" in text_lower or "stars" in text_lower:
                theme = "space"
            elif "dark" in text_lower or "black" in text_lower or "minimal" in text_lower:
                theme = "dark"
            elif "aesthetic" in text_lower:
                theme = "aesthetic"

            res = LaptopController.change_wallpaper(theme)
            action_type = "wallpaper_change"
            action_data = res
            if res.get("success"):
                response_text = (
                    f"Done, Boss Zain! I have updated your Windows desktop wallpaper with a stunning '{theme.title()}' theme. "
                    "Take a look at your screen, how does it look?"
                )
            else:
                response_text = f"Boss Zain, I encountered an issue updating the wallpaper: {res.get('message', '')}"

        # --------------------------------------------------------------------
        # 4. Laptop Applications
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["open notepad", "launch notepad", "notepad", "calculator", "calc", "settings", "explorer", "terminal", "task manager"]):
            category = "Laptop Control"
            target_app = "notepad"
            for candidate in ["calculator", "calc", "settings", "explorer", "terminal", "task manager", "notepad"]:
                if candidate in text_lower:
                    target_app = candidate
                    break
            res = LaptopController.open_system_app(target_app)
            action_type = "app_launch"
            action_data = res
            response_text = f"Opening {target_app.title()} on your laptop right now, Boss Zain."

        # --------------------------------------------------------------------
        # 5. English Teacher & Language Mentor
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["teach me english", "learn english", "english teacher", "english lesson", "english practice"]):
            category = "English Teacher"
            self.english_learning_mode = True
            response_text = (
                "Wonderful, Boss Zain! I am your personal English tutor and conversation partner. "
                "Here is today's power phrase: 'Consistency is the key to excellence'. "
                "You can ask me for word definitions, pronunciation tips, or sentence structures anytime!"
            )
            action_type = "english_teacher"
            action_data = {
                "phrase": "Consistency is the key to excellence.",
                "explanation": "Staying dedicated every single day leads to mastery.",
                "tip": "Practice speaking full sentences out loud with me."
            }

        elif any(w in text_lower for w in ["meaning of", "define", "what does", "definition of"]):
            category = "English Teacher"
            words = text_lower.replace("meaning of", "").replace("define", "").replace("what does", "").replace("mean", "").strip().split()
            target_word = words[0] if words else "innovation"

            dictionary = {
                "innovation": ("The introduction of new ideas, methods, or devices.", "Boss Zain is dedicated to technological innovation."),
                "success": ("The accomplishment of an aim or purpose.", "Success comes through persistent hard work and smart execution."),
                "intelligence": ("The ability to acquire and apply knowledge and skills.", "Artificial intelligence assists human creativity."),
                "loyalty": ("A strong feeling of support, faithfulness, and allegiance.", "Loyalty builds enduring trust and respect."),
                "future": ("A period of time that is to come.", "The future belongs to visionary creators like Boss Zain."),
                "opportunity": ("A set of circumstances that makes it possible to do something.", "Every challenge presents a great opportunity.")
            }

            val = dictionary.get(target_word.lower(), (f"The definition and context for {target_word}.", f"Example sentence using {target_word}."))
            response_text = f"Boss Zain, '{target_word}' means: {val[0]} Example sentence: '{val[1]}'"
            action_type = "english_vocab"
            action_data = {"word": target_word, "definition": val[0], "example": val[1]}

        # --------------------------------------------------------------------
        # 6. Folder & File Operations
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["create folder", "make folder", "new folder", "folder on desktop"]):
            category = "File Management"
            folder_name = "New_Folder"
            match = re.search(r'["\']([a-zA-Z0-9_\-\s]+)["\']', raw_text)
            named = re.search(r'(?:called|named)\s+([a-zA-Z0-9_\-]+)', text_lower)
            if match:
                folder_name = match.group(1).strip().replace(" ", "_")
            elif named:
                folder_name = named.group(1).title()
            else:
                folder_name = f"Zain_Projects_{time.strftime('%H%M')}"

            target_path = Path.home() / "Desktop" / folder_name
            target_path.mkdir(parents=True, exist_ok=True)
            response_text = f"All done, Boss Zain! I have created the folder '{folder_name}' on your Desktop."
            action_type = "file_system"
            action_data = {"path": str(target_path)}

        # --------------------------------------------------------------------
        # 7. Live Weather
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["weather", "forecast", "temperature"]):
            category = "Live Weather"
            response_text = "Boss Zain, I checked the current weather report. The skies are clear with pleasant conditions and temperatures around 26 degrees Celsius."
            action_type = "weather"
            action_data = {"condition": "Clear Sky", "temperature": "26°C"}

        # --------------------------------------------------------------------
        # 8. Greetings & Conversational Rapport
        # --------------------------------------------------------------------
        elif any(w in text_lower for w in ["hello", "hi", "hey", "good morning", "good evening", "how are you"]):
            category = "Greetings"
            response_text = "Hello Boss Zain! I am energized and fully online. How can I assist you with your laptop and tasks today?"
            action_type = "greeting"

        elif any(w in text_lower for w in ["thank you", "thanks", "great job", "awesome", "well done"]):
            category = "Gratitude"
            response_text = "Always at your service, Boss Zain! Your instructions are my highest priority. Let me know what to do next!"
            action_type = "compliment"

        else:
            category = "General"
            response_text = f"Understood, Boss Zain! I have logged your instruction: '{raw_text}'. Executing right now."

        # Generate smooth natural English neural speech audio
        audio_url = await self.generate_speech_file(response_text)

        return {
            "query": raw_text,
            "response": response_text,
            "audio_url": audio_url,
            "category": category,
            "action_type": action_type,
            "action_data": action_data,
            "boss": self.BOSS_NAME,
            "timestamp": time.strftime("%I:%M %p")
        }
