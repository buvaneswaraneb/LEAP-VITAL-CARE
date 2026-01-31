from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time 
import random
import subprocess
# from API_CALL import send_warning

app = Flask(__name__)
CORS(app)
 
ESP32_URL = "{ESP_32_IP}/getData" # Replace with ESP32 IP
ESP32_TOUCH_URL = "http://{ESP_32_IP}/getTouch" # Replace with ESP32 IP

# 🔹 Store last touch state
last_touch = False
last_touch_time = 0

# 🔹 Store user state with acknowledgment tracking
user_state = {
    "distress": False,
    "help": False,
    "distress_acknowledged": False,
    "help_acknowledged": False,
    "distress_timestamp": None,
    "help_timestamp": None
}

# 🔹 Store user location
user_location = {
    "longitude": None,
    "latitude": None
}

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

    # 🔹 Get touch state from ESP32
    try:
        t = requests.get(ESP32_TOUCH_URL, timeout=2)
        touch_data = t.json()
        esp_touch = touch_data.get("touched", False)
    except Exception as e:
        print("ESP32 touch offline:", e)
        esp_touch = False

    # 🔹 If ESP32 touch is true, trigger warning
    if esp_touch:
        print("touched")
        warning_msg = "⚠️⚠️⚠️⚠️⚠️🚨 Your Patient Requesting For Help ! ⚠️⚠️⚠️⚠️"
        print(warning_msg)
        # send_warning(warning_msg)  # Commented out for now
        
    return jsonify({
        "temperature": 5 + esp_data.get("temperature", 0),
        "bpm": random.randint(80, 100),
        "beat": esp_data.get("beat", False),
        "touched": esp_touch
    })


# ===============================
# USER LOCATION ENDPOINT (POST)
# ===============================
@app.route("/api/usr/location", methods=["POST", "OPTIONS"])
def receive_user_location():
    global user_location
    
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        
        if data and "longitude" in data and "latitude" in data:
            user_location["longitude"] = data["longitude"]
            user_location["latitude"] = data["latitude"]
            
            print(f"📍 User Location Updated: {user_location['latitude']}, {user_location['longitude']}")
            
            # Send alert if user is in distress/help mode and not acknowledged
            if (user_state.get("distress") and not user_state.get("distress_acknowledged")) or \
               (user_state.get("help") and not user_state.get("help_acknowledged")):
                alert_msg = f"🚨 ALERT: User needs assistance at location: {user_location['latitude']}, {user_location['longitude']}"
                print(alert_msg)
                # send_warning(alert_msg)  # Commented out for now
            
            return jsonify({
                "status": "success",
                "message": "Location received",
                "location": user_location
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid location data"
            }), 400
            
    except Exception as e:
        print(f"Error receiving location: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ===============================
# USER DETAILS ENDPOINT (POST)
# ===============================
@app.route("/api/usr/details", methods=["POST", "OPTIONS"])
def receive_user_details():
    global user_state
    
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        
        if data and "distress" in data and "help" in data:
            # 🔹 Only set to True if new signal, don't reset to False until acknowledged
            if data["distress"] and not user_state["distress"]:
                user_state["distress"] = True
                user_state["distress_acknowledged"] = False
                user_state["distress_timestamp"] = time.time()
                print(f"🚨 NEW DISTRESS SIGNAL - Timestamp: {user_state['distress_timestamp']}")
                
                distress_msg = f"⚠️ DISTRESS SIGNAL from user at location: {user_location.get('latitude', 'Unknown')}, {user_location.get('longitude', 'Unknown')}"
                print(distress_msg)
                # send_warning(distress_msg)
            
            if data["help"] and not user_state["help"]:
                user_state["help"] = True
                user_state["help_acknowledged"] = False
                user_state["help_timestamp"] = time.time()
                print(f"🆘 NEW HELP REQUEST - Timestamp: {user_state['help_timestamp']}")
                
                help_msg = f"🆘 HELP REQUEST from user at location: {user_location.get('latitude', 'Unknown')}, {user_location.get('longitude', 'Unknown')}"
                print(help_msg)
                # send_warning(help_msg)
            
            print(f"📊 Current State: Distress={user_state['distress']} (Ack={user_state['distress_acknowledged']}), Help={user_state['help']} (Ack={user_state['help_acknowledged']})")
            
            return jsonify({
                "status": "success",
                "message": "User details received",
                "state": {
                    "distress": user_state["distress"],
                    "help": user_state["help"]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid user details"
            }), 400
            
    except Exception as e:
        print(f"Error receiving user details: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ===============================
# GET CURRENT USER STATE (GET)
# ===============================
@app.route("/api/usr/status", methods=["GET", "OPTIONS"])
def user_status():
    """Endpoint to check current user state and location"""
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    return jsonify({
        "state": {
            "distress": user_state["distress"],
            "help": user_state["help"]
        },
        "location": user_location
    })


# ===============================
# ACKNOWLEDGE ALERT (POST) - NEW ENDPOINT
# ===============================
@app.route("/api/usr/acknowledge", methods=["POST", "OPTIONS"])
def acknowledge_alert():
    """Endpoint for website to acknowledge and clear alerts"""
    global user_state
    
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        
        if data:
            if data.get("distress_ack"):
                user_state["distress"] = False
                user_state["distress_acknowledged"] = True
                print("✅ Distress signal ACKNOWLEDGED and CLEARED")
                
            if data.get("help_ack"):
                user_state["help"] = False
                user_state["help_acknowledged"] = True
                print("✅ Help request ACKNOWLEDGED and CLEARED")
            
            return jsonify({
                "status": "success",
                "message": "Alert acknowledged",
                "state": {
                    "distress": user_state["distress"],
                    "help": user_state["help"]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid acknowledgment data"
            }), 400
            
    except Exception as e:
        print(f"Error acknowledging alert: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)