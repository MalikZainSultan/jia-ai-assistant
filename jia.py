#!/usr/bin/env python3
"""
Jia - Intelligent Conversational Personal Assistant & Robot
Boss: Zain Sultan
Features:
- Futuristic Web Dashboard (Holographic AI Orb & Soundwave)
- Hands-free Voice Input (Microphone Speech Recognition)
- High-fidelity Neural Voice (edge-tts Urdu & English)
- Direct Windows Laptop Control (Chrome, Edge, Wallpaper, Apps, Files)
- English Teacher Mode
Author: Lead AI Systems Engineer
"""

import os
import sys
import time
import asyncio
import threading
import webbrowser
from pathlib import Path

from jia_brain import JiaBrain
from laptop_control import LaptopController

# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# UTF-8 stdout configuration for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def banner():
    art = """
\033[96m\033[1m
       .---.          
      /     \\         [ J I A ]
     | () () |        Intelligent Personal Assistant & Autonomous Robot
      \\  -  /         Dedicated Exclusively to Boss Zain Sultan
       '---'          v2.0 • Holographic Dashboard & Laptop Controller
\033[0m"""
    print(art)


def launch_web_dashboard(port: int = 5050):
    """Starts the Flask server and opens the browser interface."""
    from server import app
    
    banner()
    print(f"\033[92m\033[1mHello Boss Zain Sultan! Jia is online and ready.\033[0m")
    print(f"\033[94mOpening Futuristic AI Dashboard at: http://127.0.0.1:{port}\033[0m")
    print("\033[90m(Microphone listening, neural voice synthesis, and laptop control enabled)\033[0m\n")

    def _open_tab():
        time.sleep(1.2)
        webbrowser.open(f"http://127.0.0.1:{port}")

    threading.Thread(target=_open_tab, daemon=True).start()
    app.run(host="0.0.0.0", port=port, debug=False)


async def cli_chat_turn(brain: JiaBrain, user_msg: str):
    """Processes a single conversational turn in the CLI."""
    res = await brain.process_user_intent(user_msg)
    print(f"\n\033[92m\033[1mJia > {res['response']}\033[0m")
    if res.get("action_data"):
        print(f"\033[90m[Action: {res.get('action_type')}] {res.get('action_data')}\033[0m")


def run_cli_mode():
    """Interactive CLI mode."""
    banner()
    brain = JiaBrain()
    print("\033[92m\033[1mHello Boss Zain Sultan! I am Jia, your automation assistant. What should I do next?\033[0m\n")

    while True:
        try:
            cmd = input("\033[96m\033[1mZain Boss > \033[0m").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\033[93mShutting down. Goodbye Boss Zain!\033[0m")
            break

        if not cmd:
            continue
        if cmd.lower() in ["exit", "quit", "q"]:
            print("\033[92mGoodbye Boss! Ready whenever you need me next.\033[0m")
            break

        asyncio.run(cli_chat_turn(brain, cmd))


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode()
    elif "--chat" in sys.argv:
        brain = JiaBrain()
        idx = sys.argv.index("--chat")
        query = " ".join(sys.argv[idx + 1:])
        print(f"Boss: {query}")
        asyncio.run(cli_chat_turn(brain, query))
    elif "--test-voice" in sys.argv:
        brain = JiaBrain()
        print("Testing Neural Urdu & English voices for Boss Zain...")
        asyncio.run(brain.process_user_intent("Salam Jia, tumhara boss kaun hai?"))
        print("Voice generation complete.")
    else:
        # Default mode: Launch Futuristic Web Dashboard for Boss Zain Sultan
        launch_web_dashboard(port=5050)
