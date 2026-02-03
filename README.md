# LEAP VITAL CARE

**IoT-Based Real-Time Patient Monitoring and Emergency Alert System**

LEAP VITAL CARE is a comprehensive healthcare monitoring platform that integrates ESP32 microcontroller sensors with a Flask backend server and responsive web interfaces to enable continuous patient vital sign tracking, GPS location monitoring, and emergency alert capabilities for healthcare providers and caregivers.

---

## Table of Contents

- [System Overview](#system-overview)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Technical Stack](#technical-stack)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage Instructions](#usage-instructions)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [Future Enhancements](#future-enhancements)

---

## System Overview

LEAP VITAL CARE addresses the critical need for remote patient monitoring by combining edge computing (ESP32), backend processing (Flask), and secure remote access (ngrok) to create a complete healthcare monitoring solution. The system enables real-time tracking of vital signs, emergency response capabilities, and location-based services for patient safety.

### Primary Use Cases

**Remote Patient Monitoring**
- Continuous vital sign tracking for elderly care
- Post-operative patient monitoring at home
- Chronic disease management
- Telemedicine support

**Emergency Response**
- Fall detection and emergency alerts
- Location tracking for wandering patients
- Direct communication channel to caregivers
- Real-time health status updates

**Healthcare Provider Tools**
- Multi-patient dashboard monitoring
- Historical data analysis through charts
- Alert management system
- Geographic patient tracking

---

## System Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      LEAP VITAL CARE SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘

[Hardware Layer]
ESP32 Development Board
├── Temperature Sensor
├── Heart Rate Sensor (BPM)
├── Capacitive Touch Sensor
└── WiFi Module
         │
         │ HTTP/JSON over WiFi (10.60.107.150)
         ↓
[Application Layer]
Flask Backend Server (localhost:8000)
├── /api/data - Vital signs endpoint
├── /api/usr/status - Emergency status endpoint
├── /api/usr/location - GPS coordinates endpoint
└── CORS handling & data processing
         │
         │ ngrok HTTPS Tunnel
         ↓
[Presentation Layer]
┌─────────────────────┬─────────────────────┐
│   Admin Dashboard   │  Patient Interface  │
│  (Medical Staff)    │  (End User)         │
├─────────────────────┼─────────────────────┤
│ - Vital monitoring  │ - Self-monitoring   │
│ - Alert management  │ - Emergency buttons │
│ - GPS tracking      │ - Location sharing  │
│ - Patient data      │ - Status display    │
└─────────────────────┴─────────────────────┘
```

### Data Flow Sequence

**Vital Signs Monitoring Flow:**
1. ESP32 sensors capture temperature and heart rate
2. Data transmitted via HTTP to Flask server
3. Flask processes and validates data
4. Admin dashboard polls `/api/data` every 2 seconds
5. Charts and displays update in real-time
6. Historical data maintained (last 20 readings)

**Emergency Alert Flow:**
1. Patient presses DISTRESS or HELP button
2. Browser sends POST to `/api/usr/status`
3. Flask stores emergency state
4. Admin dashboard detects alert (5-second polling)
5. Audio-visual popup notification triggered
6. Location data retrieved and displayed on map

**Location Tracking Flow:**
1. Patient interface requests geolocation permission
2. GPS coordinates sent to `/api/usr/location` every 30 seconds
3. Flask stores latest position
4. Admin dashboard fetches location every 10 seconds
5. Google Maps embedded iframe displays patient location

---

## Core Features

### Admin Dashboard (index_updated.html)

**Real-Time Vital Sign Monitoring**
- Temperature display with historical trend chart (last 20 points)
- Heart rate (BPM) display with historical trend chart
- 2-second automatic refresh interval
- Connection status indicator
- Anomaly detection and threshold alerts

**GPS Location Tracking**
- Embedded Google Maps interface
- Real-time coordinate updates (latitude/longitude)
- 10-second automatic refresh
- Fullscreen map toggle
- Coordinate precision: 6 decimal places

**Emergency Alert Management**
- Active monitoring every 5 seconds
- Two-tier alert system:
  - DISTRESS signal (warning level)
  - HELP request (critical level)
- Audio notification with popup alerts
- Patient location context in alerts
- Alert acknowledgment system

**Patient Management**
- User registration and login
- Patient profile database
- Photo capture capability (ESP32 camera)
- Session management

### Patient Interface (userView_production.html)

**Vital Signs Self-Monitoring**
- Current temperature reading
- Current heart rate (BPM)
- 5-second automatic refresh
- Connection status indicator
- Simple, accessible interface design

**Emergency Controls**
- Yellow "DISTRESS" button - Non-critical assistance
- Red "REQUEST HELP" button - Critical emergency
- Confirmation dialogs prevent accidental activation
- Visual feedback on button press
- One-touch emergency activation

**Location Services**
- Automatic geolocation permission request
- Continuous GPS transmission (30-second intervals)
- Real-time coordinate display
- Privacy-conscious implementation
- Battery-optimized tracking

---

## Technical Stack

### Backend Technologies

**Flask Server (flask_server_fixed.py)**
- Python 3.7+
- Flask 2.0+ web framework
- Flask-CORS for cross-origin requests
- Requests library for ESP32 communication
- In-memory data storage (future: database integration)

**Key Backend Functions:**
```python
# Vital signs retrieval
GET /api/data
→ Returns: {"temperature": float, "bpm": int}

# Emergency status handling
POST /api/usr/status
→ Accepts: {"distress": bool, "help": bool}
→ Returns: Status confirmation

# Location updates
POST /api/usr/location
→ Accepts: {"latitude": float, "longitude": float}
→ Returns: Location stored confirmation
```

### Frontend Technologies

**Admin Dashboard**
- HTML5/CSS3/JavaScript
- Chart.js for data visualization
- Google Maps JavaScript API
- Fetch API for AJAX requests
- Responsive CSS Grid layout

**Patient Interface**
- Mobile-first responsive design
- Geolocation API
- Touch-optimized controls
- Minimal JavaScript dependencies
- Accessibility-focused UI

### Hardware Stack

**ESP32 Microcontroller**
- Dual-core Xtensa 32-bit processor
- WiFi 802.11 b/g/n connectivity
- 520 KB SRAM
- 4 MB Flash storage
- Multiple GPIO pins for sensors

**Sensors**
- Temperature sensor (analog/digital)
- Heart rate sensor (optical/PPG)
- Capacitive touch sensor
- Optional: Camera module for patient photos

---

## Hardware Requirements

### Minimum Hardware

**Microcontroller Platform:**
- ESP32 development board (WROOM-32 or equivalent)
- USB cable for programming and power
- Breadboard for prototyping (optional)

**Sensors:**
- Temperature sensor (DS18B20, DHT11, or similar)
- Heart rate sensor (MAX30100, MAX30102, or similar)
- Capacitive touch sensor or button
- Connecting wires and resistors

**Network:**
- WiFi router/access point (2.4 GHz)
- Stable internet connection for ngrok
- Local network access

### Recommended Hardware

**Enhanced Setup:**
- ESP32-CAM for patient photo capture
- MAX30102 pulse oximeter (improved accuracy)
- DS18B20 waterproof temperature probe
- Rechargeable battery pack for portability
- 3D-printed enclosure

---

## Software Requirements

### Development Environment

**Required Software:**
- Python 3.7 or higher
- Arduino IDE 1.8.10+ or PlatformIO
- ngrok account (free tier sufficient)
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Python Dependencies:**
```bash
flask>=2.0.0
flask-cors>=3.0.10
requests>=2.26.0
```

### Operating System Support

**Server Compatibility:**
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 20.04+, Debian, Fedora)
- Raspberry Pi OS

**Client Compatibility:**
- Any device with modern web browser
- Mobile devices (iOS 12+, Android 8+)
- Tablets and desktop computers

---

## Installation Guide

### Step 1: ESP32 Hardware Setup

**1.1 Install Arduino IDE**
```bash
# Download from https://www.arduino.cc/en/software
# Or use package manager:

# macOS
brew install arduino

# Linux (Ubuntu/Debian)
sudo apt-get install arduino
```

**1.2 Configure ESP32 Board Support**
- Open Arduino IDE
- Go to File → Preferences
- Add ESP32 board manager URL:
  ```
  https://dl.espressif.com/dl/package_esp32_index.json
  ```
- Tools → Board → Boards Manager
- Search "ESP32" and install "ESP32 by Espressif Systems"

**1.3 Connect Sensors to ESP32**

*Temperature Sensor (DS18B20):*
```
VCC  → 3.3V
GND  → GND
DATA → GPIO (configured in code)
```

*Heart Rate Sensor (MAX30100):*
```
VCC → 3.3V
GND → GND
SDA → GPIO21
SCL → GPIO22
```

*Touch Sensor:*
```
OUT → GPIO (configured in code)
VCC → 3.3V
GND → GND
```

**1.4 Upload ESP32 Code**
- Configure WiFi credentials in ESP32 sketch
- Select board: Tools → Board → ESP32 Dev Module
- Select port: Tools → Port → [Your ESP32 Port]
- Upload code to ESP32
- Open Serial Monitor (115200 baud)
- Note the assigned IP address (e.g., 10.60.107.150)

### Step 2: Python Environment Setup

**2.1 Create Virtual Environment (Recommended)**
```bash
# Navigate to project directory
cd leap-vital-care

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**2.2 Install Dependencies**
```bash
# Install required packages
pip install flask flask-cors requests

# Or use requirements.txt if provided:
pip install -r requirements.txt
```

### Step 3: Flask Server Configuration

**3.1 Update ESP32 IP Addresses**

Edit `flask_server_fixed.py`:
```python
# Around lines 11-12
ESP32_URL = "http://YOUR_ESP32_IP/getData"
ESP32_TOUCH_URL = "http://YOUR_ESP32_IP/getTouch"

# Example:
ESP32_URL = "http://10.60.107.150/getData"
ESP32_TOUCH_URL = "http://10.60.107.150/getTouch"
```

**3.2 Configure Port (Optional)**

Default port is 8000. To change:
```python
# flask_server_fixed.py - Last line
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

**3.3 Start Flask Server**
```bash
python flask_server_fixed.py

# Expected output:
# * Running on http://0.0.0.0:8000
# * Running on http://192.168.1.x:8000
```

### Step 4: ngrok Configuration

**4.1 Install ngrok**

*Windows:*
```bash
# Download from https://ngrok.com/download
# Or use Chocolatey:
choco install ngrok
```

*macOS:*
```bash
brew install ngrok/ngrok/ngrok
```

*Linux:*
```bash
# Download and install
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

**4.2 Create ngrok Account**
- Visit https://dashboard.ngrok.com/signup
- Sign up for free account
- Copy authentication token

**4.3 Configure Authentication**
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

**4.4 Start ngrok Tunnel**
```bash
ngrok http 8000

# Output example:
# Forwarding   https://abc123-xyz789.ngrok-free.app -> http://localhost:8000
```

**4.5 Copy ngrok URL**
- Copy the HTTPS forwarding URL
- Example: `https://nonsignificantly-bilgier-particia.ngrok-free.app`

### Step 5: Web Interface Configuration

**5.1 Update Admin Dashboard**

Edit `index_updated.html`:

```javascript
// Find around line 597
const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/data';

// Find around line 700 (checkUserAlerts function)
const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/usr/status';

// Find around line 1238 (fetchUserLocation function)
const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/usr/status';

// Replace YOUR_NGROK_URL with your actual ngrok URL
```

**5.2 Update Patient Interface**

Edit `userView_production.html`:

```javascript
// Find around line 301
const API_BASE = 'https://YOUR_NGROK_URL.ngrok-free.app/api';

// Replace with your ngrok URL
```

**5.3 Open Interfaces**
- Open `index_updated.html` in browser (Admin Dashboard)
- Open `userView_production.html` in browser or mobile device (Patient Interface)

---

## Configuration

### Update Intervals

**Admin Dashboard:**
```javascript
// Vital signs refresh (default: 2 seconds)
// index_updated.html, around line 1095
const intervalId = setInterval(fetchData, 2000);

// Alert checking (default: 5 seconds)
// index_updated.html, around line 723
setInterval(checkUserAlerts, 5000);

// Location updates (default: 10 seconds)
// index_updated.html, around line 1261
setInterval(fetchUserLocation, 10000);
```

**Patient Interface:**
```javascript
// Vital signs refresh (default: 5 seconds)
// userView_production.html, around line 361
setInterval(fetchVitalSigns, 5000);

// Location transmission (default: 30 seconds)
// userView_production.html, around line 445
setInterval(sendLocation, 30000);
```

### Threshold Configuration

**Temperature Alerts:**
```javascript
// index_updated.html
if (temperature > 38.5) {
  // High temperature alert
} else if (temperature < 35.0) {
  // Low temperature alert
}
```

**Heart Rate Alerts:**
```javascript
// index_updated.html
if (bpm > 120) {
  // Tachycardia alert
} else if (bpm < 50) {
  // Bradycardia alert
}
```

---

## API Documentation

### Endpoint Reference

**GET /api/data**
- **Purpose:** Retrieve current vital signs
- **Method:** GET
- **Headers:** 
  ```
  ngrok-skip-browser-warning: true
  ```
- **Response:**
  ```json
  {
    "temperature": 36.5,
    "bpm": 72
  }
  ```
- **Error Handling:**
  - ESP32 unreachable → Returns default values
  - Network timeout → Returns cached data

**POST /api/usr/status**
- **Purpose:** Send/receive emergency alerts
- **Method:** POST
- **Content-Type:** application/json
- **Request Body:**
  ```json
  {
    "distress": true,
    "help": false
  }
  ```
- **Response:**
  ```json
  {
    "status": "received",
    "distress": true,
    "help": false
  }
  ```

**POST /api/usr/location**
- **Purpose:** Update patient GPS coordinates
- **Method:** POST
- **Content-Type:** application/json
- **Request Body:**
  ```json
  {
    "latitude": 12.853794,
    "longitude": 80.175039
  }
  ```
- **Response:**
  ```json
  {
    "status": "location_updated",
    "latitude": 12.853794,
    "longitude": 80.175039
  }
  ```

**OPTIONS /api/***
- **Purpose:** CORS preflight handling
- **Method:** OPTIONS
- **Response Headers:**
  ```
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Methods: GET, POST, OPTIONS
  Access-Control-Allow-Headers: Content-Type
  ```

---

## Usage Instructions

### Admin Dashboard Operation

**Initial Setup:**
1. Ensure Flask server and ngrok are running
2. Open `index_updated.html` in web browser
3. Log in with credentials (if authentication enabled)
4. Verify connection status indicator shows "Connected"

**Monitoring Patient Vitals:**
1. Temperature and BPM display in real-time
2. Charts show last 20 data points
3. Hover over charts for specific values
4. Connection status updates automatically

**Responding to Alerts:**
1. Alert popup appears when patient triggers emergency
2. Audio notification plays
3. Review alert type (DISTRESS vs HELP)
4. Click "View Location" to see patient position on map
5. Take appropriate action

**Viewing Patient Location:**
1. Click "Show Location" button
2. Google Maps displays current patient position
3. Map refreshes every 10 seconds
4. Click fullscreen icon for expanded view
5. Coordinates displayed below map

### Patient Interface Operation

**Initial Setup:**
1. Open `userView_production.html` on patient device
2. Allow location permissions when prompted
3. Verify vital signs are displaying
4. Test emergency buttons (optional)

**Self-Monitoring:**
1. Temperature and heart rate update every 5 seconds
2. Connection status shows if system is active
3. Review personal vital signs

**Using Emergency Buttons:**
1. **DISTRESS (Yellow):** Non-critical assistance needed
   - Feeling unwell
   - Need attention but not emergency
   - Confirmation dialog appears
2. **REQUEST HELP (Red):** Critical emergency
   - Severe pain or distress
   - Fall or injury
   - Immediate assistance required
   - Confirmation dialog appears

**Location Sharing:**
- Automatic GPS transmission every 30 seconds
- Coordinates displayed at bottom of screen
- No manual action required
- Can be disabled in browser settings if needed

---

## Troubleshooting

### Common Issues and Solutions

**Problem: "Failed to fetch" error in browser**

*Solutions:*
```bash
# Check Flask server
# Terminal should show: "Running on http://0.0.0.0:8000"

# Check ngrok tunnel
# Visit http://localhost:4040 for ngrok status

# Verify ngrok URL in HTML files matches tunnel URL
```

**Problem: No vital signs displaying**

*Solutions:*
```bash
# Check ESP32 Serial Monitor for IP address and WiFi status
# Verify ESP32 IP in flask_server_fixed.py
# Test ESP32 endpoint directly:
curl http://ESP32_IP/getData
```

**Problem: Location not updating**

*Solutions:*
- Allow location permissions in browser settings
- Ensure using ngrok HTTPS URL (not http://localhost)
- Move to location with better GPS signal

**Problem: CORS errors**

*Solutions:*
```bash
# Install flask-cors
pip install flask-cors

# Verify in flask_server_fixed.py:
from flask_cors import CORS
CORS(app)
```

---

## File Structure

```
leap-vital-care/
│
├── flask_server_fixed.py          # Main Flask backend server
│   ├── /api/data                   # Vital signs endpoint
│   ├── /api/usr/status             # Emergency status endpoint
│   └── /api/usr/location           # GPS location endpoint
│
├── index_updated.html              # Admin dashboard interface
│   ├── Chart.js integration        # Data visualization
│   ├── Google Maps integration     # Location tracking
│   └── Alert management system     # Emergency notifications
│
├── userView_production.html        # Patient interface
│   ├── Vital signs display         # Self-monitoring
│   ├── Emergency buttons           # Alert triggers
│   └── GPS location sharing        # Position transmission
│
├── ESP32_Code/                     # ESP32 firmware (if included)
│   ├── sensor_readings.ino         # Main sensor code
│   ├── wifi_config.h               # WiFi configuration
│   └── api_endpoints.ino           # HTTP server endpoints
│
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
└── .gitignore                      # Git ignore rules
```

---

## Future Enhancements

### Planned Features

**Database Integration:**
- PostgreSQL or MongoDB for persistent storage
- Historical data analysis and reporting
- Patient record management
- Data export functionality (CSV, PDF)

**Enhanced Monitoring:**
- Additional vital signs (SpO2, blood pressure)
- ECG monitoring capability
- Respiratory rate tracking
- Sleep pattern analysis
- Fall detection algorithm

**Security & Compliance:**
- End-to-end encryption
- HIPAA compliance measures
- User authentication system (OAuth2)
- Two-factor authentication
- Audit logging

**Communication:**
- SMS/Email notifications to caregivers
- Push notifications to mobile devices
- Two-way video calling
- Voice alerts for emergencies
- Auto-dial emergency contacts

**Integration:**
- Hospital system integration (HL7/FHIR)
- Wearable device support (Fitbit, Apple Watch)
- Electronic Health Records (EHR) compatibility
- Telemedicine platform integration

---

## License and Disclaimer

### Medical Disclaimer

**IMPORTANT:** LEAP VITAL CARE is a prototype system designed for educational and research purposes only. This system should NOT be used as a replacement for professional medical devices, clinical-grade monitoring equipment, emergency medical services, or professional medical diagnosis/treatment.

Users must always consult qualified healthcare professionals for medical advice and not rely solely on this system for critical health decisions.

The developers and contributors assume no liability for any medical outcomes resulting from the use of this system.

### Privacy Notice

This system collects and transmits sensitive health information and location data. Users should ensure compliance with local data protection laws (GDPR, HIPAA, etc.) and implement appropriate security measures.

---

## Version Information

**Current Version:** 1.0.0  
**Release Date:** January 2026  
**Last Updated:** January 28, 2026  
**Documentation Status:** Complete  
**Maintenance:** Active  

### Version History

**v1.0.0 (January 2026) - Initial Release**
- ESP32 sensor integration (temperature, heart rate, touch)
- Flask backend with RESTful API
- Admin dashboard with real-time monitoring
- Patient interface with emergency buttons
- GPS location tracking
- Emergency alert system
- Google Maps integration
- Real-time data visualization with Chart.js
- ngrok HTTPS tunneling
- CORS support for remote access

---

**Built for Better Healthcare**

*LEAP VITAL CARE - Monitoring Vitals, Saving Lives*
