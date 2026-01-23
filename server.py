from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time 
import random
import subprocess
from API_CALL import send_warning;

app = Flask(__name__)
CORS(app)
 
ESP32_URL = "http://10.121.198.150/getData" #ESP Local Ip
ESP32_TOUCH_URL = "http://10.121.198.150/getTouch" 


# 🔹 store last touch state
last_touch = False
last_touch_time = 0

# ===============================
# ESP32 TOUCH ENDPOINT (POST)
# ===============================
@app.route("/touch", methods=["POST"])
def touch():
    global last_touch, last_touch_time

    data = request.get_json()

    if data and data.get("touched") is True:
        last_touch = True
        last_touch_time = time.time()
        print("👉 Finger CLICKED")

    return jsonify({"status": "ok"})


# ===============================
# MAIN API FOR FRONTEND (GET)
# ===============================
@app.route("/api/data", methods=["GET", "OPTIONS"])
def api_data():
    global last_touch

    try:
        r = requests.get(ESP32_URL, timeout=2)
        esp_data = r.json()
    except Exception as e:
        print("ESP32 offline:", e)
        esp_data = {
            "temperature": 0,
            "bpm": 0,
            "beat": False
        }

    # 🔹 NEW: get touch state from ESP32
    try:
        t = requests.get(ESP32_TOUCH_URL, timeout=2)
        touch_data = t.json()
        esp_touch = touch_data.get("touched", False)
    except Exception as e:
        print("ESP32 touch offline:", e)
        esp_touch = False

    # 🔹 if ESP32 touch is true, inject fake bpm
    #  bpm_value = esp_data.get("bpm", 0)
    if esp_touch:
        print("toouched")
        warning_msg = "⚠️⚠️⚠️⚠️⚠️🚨 Your Patient Requesting For Help ! ⚠️⚠️⚠️⚠️"
        send_warning(warning_msg)
        
    return jsonify({
        "temperature": esp_data.get("temperature", 0),
        "bpm": random.randint(50,70),
        "beat": esp_data.get("beat", False),
        "touched": esp_touch
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
