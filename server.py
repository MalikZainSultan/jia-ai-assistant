"""
Jia Web Server & Local Desktop Bridge
Flask Server providing the Futuristic Dashboard and Windows Control
"""

import os
import sys
import asyncio
import webbrowser
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file

from jia_brain import JiaBrain
from laptop_control import LaptopController

app = Flask(__name__, template_folder="templates", static_folder="static")
brain = JiaBrain()

# Ensure static directories exist
Path("static/audio").mkdir(parents=True, exist_ok=True)
Path("wallpapers").mkdir(parents=True, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/command", methods=["POST"])
def handle_command():
    data = request.get_json() or {}
    cmd_text = data.get("command", "").strip()
    if not cmd_text:
        return jsonify({"error": "Empty command"}), 400

    # Run asynchronous intent processing in an event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(brain.process_user_intent(cmd_text))
    loop.close()

    return jsonify(result)


@app.route("/api/status", methods=["GET"])
def get_status():
    telemetry = LaptopController.get_system_telemetry()
    return jsonify(telemetry)


@app.route("/api/wallpaper/preview", methods=["GET"])
def get_wallpaper_preview():
    # Return the latest downloaded wallpaper or placeholder
    wallpapers = list(Path("wallpapers").glob("*.jpg"))
    if wallpapers:
        latest = max(wallpapers, key=os.path.getmtime)
        return send_file(str(latest), mimetype="image/jpeg")
    
    # Return default placeholder
    placeholder = Path("static/preview_placeholder.jpg")
    if placeholder.exists():
        return send_file(str(placeholder), mimetype="image/jpeg")
    return jsonify({"error": "No wallpaper applied yet"}), 404


def open_browser_tab():
    import time
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5050")


if __name__ == "__main__":
    port = 5050
    print(f"\n[JIA CORE] Starting Futuristic AI Assistant Server on http://127.0.0.1:{port}")
    print("[JIA CORE] Dedicated Personal AI Assistant for Boss Zain Sultan\n")
    
    # Launch browser automatically for Boss Zain
    threading.Thread(target=open_browser_tab, daemon=True).start()
    
    # Run server
    app.run(host="0.0.0.0", port=port, debug=False)
