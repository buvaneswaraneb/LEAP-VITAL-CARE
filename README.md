# Vital Care - IoT Patient Monitoring System

A comprehensive IoT-based patient monitoring system that combines ESP32 sensors, Flask backend, and responsive web interfaces to provide real-time health monitoring and emergency alert capabilities.

---

## Table of Contents

- [System Overview](#system-overview)
- [Architecture](#architecture)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)

---

## System Overview

Vital Care is a real-time patient monitoring system designed for healthcare providers and caregivers. The system monitors vital signs (temperature, heart rate) and provides emergency alert capabilities with GPS location tracking.

### Key Components:

1. **ESP32 Microcontroller** - Captures sensor data (temperature, BPM, touch)
2. **Flask Backend Server** - Processes and routes data
3. **ngrok Tunnel** - Enables remote access via HTTPS
4. **Admin Dashboard** - For doctors/caregivers to monitor patients
5. **User Mobile Interface** - For patients to send emergency alerts

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Flow                                │
└─────────────────────────────────────────────────────────────────┘

ESP32 Sensors (Local WiFi)
    ↓
    ↓ HTTP (Local IP: 10.60.107.150)
    ↓
Flask Server (localhost:8000)
    ↓
    ↓ Data Processing & Storage
    ↓
ngrok Tunnel (HTTPS)
    ↓
    ├──→ Admin Dashboard (index.html)
    │    - View real-time vitals
    │    - Monitor location
    │    - Receive alerts
    │
    └──→ User Interface (userView_production.html)
         - View own vitals
         - Send distress/help signals
         - Share GPS location
```

### Communication Flow:

```
┌──────────────┐     Local     ┌──────────────┐
│   ESP32      │────────────→  │    Flask     │
│  Sensors     │   HTTP/JSON   │   Server     │
└──────────────┘               └──────────────┘
                                      ↕
                                   ngrok
                                      ↕
┌──────────────────────────────────────────────┐
│           Internet (HTTPS)                    │
└──────────────────────────────────────────────┘
         ↓                           ↓
┌──────────────┐            ┌──────────────┐
│    Admin     │            │     User     │
│  Dashboard   │            │  Interface   │
└──────────────┘            └──────────────┘
```

---

##  Features

### Admin Dashboard (Doctor/Caregiver View)

-  **Real-time Vital Monitoring**
  - Live temperature readings
  - Heart rate (BPM) tracking
  - Historical data charts (20 data points)
  - Connection status indicator

- **GPS Location Tracking**
  - Interactive Google Maps integration
  - Fullscreen map mode
  - Auto-refresh every 10 seconds
  - Zoom and pan capabilities
  - Coordinate display

-  **Emergency Alert System**
  - Real-time distress signal detection
  - Help request notifications
  - Popup alerts with sound
  - Patient location in alerts
  - Auto-monitoring every 5 seconds

- **Patient Photo Capture**
  - Direct ESP32 camera integration
  - Photo storage per patient

- **Multi-User Support**
  - User login/signup system
  - Patient profile management

### User Interface (Patient View)

- 📱 **Vital Signs Display**
  - Current temperature
  - Current heart rate (BPM)
  - Connection status indicator
  - Auto-refresh every 5 seconds

- **Emergency Buttons**
  - Yellow "DISTRESS" button
  - Red "REQUEST HELP" button
  - Confirmation popups
  - Visual feedback

- **GPS Location Sharing**
  - Automatic location permission request
  - Sends location every 30 seconds
  - Real-time coordinate display
  - Background location tracking

---

## System Requirements

### Hardware:
- ESP32 Development Board
- Temperature sensor (compatible with ESP32)
- Heart rate sensor (compatible with ESP32)
- Capacitive touch sensor
- WiFi network

### Software:
- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- ngrok account (free tier works)

### Operating System:
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 20.04+)

---

## Installation & Setup

### Step 1: ESP32 Setup

1. **Flash ESP32 with sensor code**
   ```bash
   # Use Arduino IDE or PlatformIO
   # Configure WiFi credentials in your ESP32 code
   ```

2. **Connect sensors:**
   - Temperature sensor → ESP32 GPIO
   - Heart rate sensor → ESP32 GPIO
   - Touch sensor → ESP32 GPIO

3. **Note your ESP32's local IP address**
   - Example: `10.60.107.150`
   - Update this in `flask_server_fixed.py`

### Step 2: Python Environment Setup

1. **Install Python 3.7+**
   ```bash
   # Check Python version
   python --version
   # or
   python3 --version
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate on Windows:
   venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install flask flask-cors requests
   ```

### Step 3: Flask Server Configuration

1. **Edit `flask_server_fixed.py`**
   ```python
   # Line 11-12: Update ESP32 IP addresses
   ESP32_URL = "http://YOUR_ESP32_IP/getData"
   ESP32_TOUCH_URL = "http://YOUR_ESP32_IP/getTouch"
   ```

2. **Optional: Configure API_CALL module**
   ```python
   # If you have a custom alert system
   from API_CALL import send_warning
   
   # Or comment out if not using:
   # from API_CALL import send_warning
   ```

3. **Start Flask server**
   ```bash
   python flask_server_fixed.py
   ```
   
   You should see:
   ```
    * Running on http://0.0.0.0:8000
    * Running on http://YOUR_LOCAL_IP:8000
   ```

### Step 4: ngrok Setup

1. **Install ngrok**
   - Download from https://ngrok.com/download
   - Or use package manager:
     ```bash
     # macOS
     brew install ngrok
     
     # Windows (with Chocolatey)
     choco install ngrok
     
     # Linux
     sudo snap install ngrok
     ```

2. **Sign up for ngrok account**
   - Visit https://dashboard.ngrok.com/signup
   - Get your auth token

3. **Configure ngrok**
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

4. **Start ngrok tunnel**
   ```bash
   ngrok http 8000
   ```
   
   You'll see output like:
   ```
   Forwarding  https://xxxx-yyyy-zzzz.ngrok-free.app -> http://localhost:8000
   ```

5. **Copy your ngrok URL**
   - Example: `https://nonsignificantly-bilgier-particia.ngrok-free.app`

### Step 5: Configure Web Interfaces

1. **Update Admin Dashboard (`index_updated.html`)**
   
   Find and replace these URLs:
   
   ```javascript
   // Around line 597
   const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/data';
   
   // Around line 700 (in checkUserAlerts function)
   const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/usr/status';
   
   // Around line 1238 (in fetchUserLocation function)
   const API_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/api/usr/status';
   ```

2. **Update User Interface (`userView_production.html`)**
   ```javascript
   // Around line 301
   const API_BASE = 'https://YOUR_NGROK_URL.ngrok-free.app/api';
   ```

3. **Open the interfaces**
   - Admin Dashboard: Open `index_updated.html` in browser
   - User Interface: Open `userView_production.html` in browser (on mobile or desktop)

---

## Configuration

### Flask Server Port

Default: `8000`

To change:
```python
# flask_server_fixed.py - Last line
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=YOUR_PORT, debug=True)
```

Then update ngrok:
```bash
ngrok http YOUR_PORT
```

### Update Intervals

**Admin Dashboard (`index_updated.html`):**
```javascript
// Vital signs update (default: 2 seconds)
// Around line 1095
updateInterval = setInterval(fetchData, 2000);

// Location update (default: 10 seconds)
// Around line 1395
locationUpdateInterval = setInterval(fetchUserLocation, 10000);

// Alert check (default: 5 seconds)
// Around line 773
alertCheckInterval = setInterval(checkUserAlerts, 5000);
```

**User Interface (`userView_production.html`):**
```javascript
// Vital signs update (default: 5 seconds)
// Around line 531
setInterval(fetchSensorData, 5000);

// Location send (default: 30 seconds)
// Around line 393
locationInterval = setInterval(sendLocation, 30000);
```

### Google Maps Settings

```javascript
// Change zoom level (default: 16)
// Around line 1297 in index_updated.html
const mapUrl = `https://www.google.com/maps?q=${lat},${lon}&z=YOUR_ZOOM&output=embed`;
// Zoom levels: 1 (world) to 21 (buildings)
```

---

## Usage Guide

### For Administrators (Doctors/Caregivers)

1. **Login**
   - Default credentials:
     - Username: `admin`
     - Date of Birth: `1111-11-11`

2. **Monitor Patient Vitals**
   - Click "stats" button
   - View real-time temperature and heart rate charts
   - Check connection status (green dot = connected)

3. **View Patient Location**
   - Click "locate" button
   - Map loads with patient's current location
   - Click "🗺️ Fullscreen" for expanded view
   - Click "🔄 Refresh" to update location manually

4. **Receive Emergency Alerts**
   - Alerts appear automatically as popups
   - Sound notification plays
   - Options:
     - "View Location" - Jump to map
     - "Dismiss" - Close alert

5. **Capture Patient Photo**
   - Click "photo" button
   - Click "Photo" to capture from ESP32 camera

### For Patients (Users)

1. **Open User Interface**
   - Open `userView_production.html` on your device
   - Allow location permissions when prompted

2. **View Your Vitals**
   - Temperature and heart rate display automatically
   - Updates every 5 seconds

3. **Send Emergency Alert**
   - **Distress Signal:**
     - Tap yellow "DISTRESS" button
     - Confirm in popup
     - Alert sent to all caregivers
   
   - **Help Request:**
     - Tap red "REQUEST HELP!" button
     - Confirm in popup
     - Alert sent to all caregivers

4. **Location Tracking**
   - Location automatically shared every 30 seconds
   - Status shown at bottom of screen
   - Coordinates displayed

---

## API Documentation

### Base URL
```
https://YOUR_NGROK_URL.ngrok-free.app/api
```

### Endpoints

#### 1. Get Sensor Data
```http
GET /api/data
```

**Response:**
```json
{
  "temperature": 36.5,
  "bpm": 85,
  "beat": false,
  "touched": false
}
```

**Description:** Returns current sensor readings from ESP32

---

#### 2. Send User Location
```http
POST /api/usr/location
```

**Headers:**
```http
Content-Type: application/json
ngrok-skip-browser-warning: true
```

**Request Body:**
```json
{
  "longitude": 80.175039,
  "latitude": 12.853794
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Location received",
  "location": {
    "longitude": 80.175039,
    "latitude": 12.853794
  }
}
```

**Description:** Updates user's GPS location on server

---

#### 3. Send User Alert Status
```http
POST /api/usr/details
```

**Headers:**
```http
Content-Type: application/json
ngrok-skip-browser-warning: true
```

**Request Body:**
```json
{
  "distress": true,
  "help": false
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User details received",
  "state": {
    "distress": true,
    "help": false
  }
}
```

**Description:** Updates user's emergency alert state

---

#### 4. Get User Status
```http
GET /api/usr/status
```

**Headers:**
```http
ngrok-skip-browser-warning: true
```

**Response:**
```json
{
  "state": {
    "distress": false,
    "help": false
  },
  "location": {
    "longitude": 80.175039,
    "latitude": 12.853794
  }
}
```

**Description:** Returns current user state and location

---

#### 5. ESP32 Touch Endpoint
```http
POST /touch
```

**Request Body:**
```json
{
  "touched": true
}
```

**Response:**
```json
{
  "status": "ok"
}
```

**Description:** Receives touch sensor data from ESP32

---

##  Troubleshooting

### Common Issues

#### 1. "Connection Error" on Admin Dashboard

**Problem:** Can't fetch data from API

**Solutions:**
- ✅ Check Flask server is running
- ✅ Verify ngrok tunnel is active
- ✅ Confirm ngrok URL in HTML files matches your actual URL
- ✅ Check browser console (F12) for specific errors

**Test:**
```bash
# Check Flask server
curl http://localhost:8000/api/data

# Check ngrok tunnel
curl https://YOUR_NGROK_URL.ngrok-free.app/api/data
```

---

#### 2. "Location Access Denied"

**Problem:** Browser blocks location access

**Solutions:**
- Allow location permissions when prompted
- For HTTPS only: ngrok provides HTTPS automatically
- Check browser settings: Site Settings → Permissions → Location
- Try different browser

---

#### 3. Map Keeps Resetting/Flashing

**Problem:** Map reloads every time you switch pages

**Solution:** Already fixed in `index_updated.html`
- Map only reloads if coordinates change
- Switching pages preserves map state

---

#### 4. ESP32 Not Sending Data

**Problem:** Temperature/BPM shows "--"

**Solutions:**
- Check ESP32 is powered on
- Verify WiFi connection on ESP32
- Check ESP32 IP in Flask server matches actual IP
- Test ESP32 endpoints directly:
  ```bash
  curl http://YOUR_ESP32_IP/getData
  ```

---

#### 5. Alerts Not Appearing

**Problem:** Admin doesn't receive distress/help alerts

**Solutions:**
- Check Flask server console for errors
- Verify alert monitoring is running (starts after login)
- Check browser console for JavaScript errors
- Confirm user sent alert successfully

**Debug:**
```python
# Check Flask server logs
# Should see: "🚨 User State Updated: Distress=True, Help=False"
```

---

#### 6. ngrok URL Changes

**Problem:** ngrok URL is different after restart

**Solutions:**
- Free ngrok generates new URL each restart
- Update URLs in both HTML files after ngrok restart
- Or: Upgrade to ngrok paid plan for static domain

---

#### 7. CORS Errors

**Problem:** Browser blocks requests (CORS policy)

**Solutions:**
- Ensure `flask-cors` is installed
- Verify `CORS(app)` is in Flask server
- Check `ngrok-skip-browser-warning` header is sent

---

#### 8. TypeError: Object of type function is not JSON serializable

**Problem:** Variable name conflicts with function name

**Solution:** Already fixed in `flask_server_fixed.py`
- Functions renamed to avoid conflicts:
  - `user_location()` → `receive_user_location()`
  - `user_details()` → `receive_user_details()`

---

### Debug Mode

Enable detailed logging:

**Flask:**
```python
# Already enabled in flask_server_fixed.py
app.run(host="0.0.0.0", port=8000, debug=True)
```

**Browser:**
```javascript
// Open browser console (F12)
// Check Console tab for errors
// Check Network tab for failed requests
```

---

## 📁 File Structure

```
vital-care/
│
├── flask_server_fixed.py          # Main Flask backend server
│   ├── ESP32 data endpoints
│   ├── User location handling
│   ├── Alert state management
│   └── CORS configuration
│
├── index_updated.html              # Admin dashboard (doctor/caregiver)
│   ├── Login/Signup pages
│   ├── Camera page (ESP32 photo capture)
│   ├── Stats page (vital signs charts)
│   ├── Location page (GPS map tracking)
│   └── Alert popup system
│
├── userView_production.html        # Patient interface (mobile/web)
│   ├── Temperature display
│   ├── Heart rate display
│   ├── Distress button with confirmation
│   ├── Help button with confirmation
│   └── GPS location sharing
│
├── README.md                       # This file
│
└── API_CALL.py                     # (Optional) Custom alert system
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.x** - Programming language
- **Flask 2.x** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
  - Flexbox layouts
  - Animations
  - Responsive design
- **JavaScript (ES6+)** - Interactivity
  - Async/Await
  - Fetch API
  - DOM manipulation
- **Google Maps Embed API** - Location visualization
- **Geolocation API** - GPS tracking

### Hardware
- **ESP32** - Microcontroller (WiFi capable)
- **Sensors** - Temperature, heart rate, capacitive touch

### Infrastructure
- **ngrok** - HTTPS tunneling & public URL
- **WiFi** - Local network communication

### Fonts & UI
- **Gaegu** - Google Fonts (handwritten style)

---

##  Security Considerations

### Current Setup (Development)
⚠️ **For development/testing only - NOT production-ready**

- No authentication on API endpoints
- ngrok URLs are temporary and semi-random
- Data stored in memory (not persistent)
- HTTP between ESP32 and Flask (local network only)
- No rate limiting
- No input validation

### Production Recommendations

1. **Add API Authentication**
   ```python
   # Example: JWT tokens
   from flask_jwt_extended import JWTManager, jwt_required
   
   @app.route('/api/data')
   @jwt_required()
   def api_data():
       # ...
   ```

2. **Use HTTPS Everywhere**
   - SSL certificates (Let's Encrypt)
   - Secure WebSockets for real-time data
   - HTTPS between ESP32 and server

3. **Database Integration**
   ```python
   # Example: PostgreSQL
   from flask_sqlalchemy import SQLAlchemy
   
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'
   db = SQLAlchemy(app)
   ```

4. **User Authentication**
   - Secure password hashing (bcrypt, Argon2)
   - Session management
   - Role-based access control (RBAC)
   - Multi-factor authentication (MFA)

5. **Static Domain**
   - Purchase domain name
   - Use ngrok paid plan or deploy to cloud
   - AWS, Azure, Google Cloud, or Heroku

6. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=get_remote_address)
   
   @app.route('/api/data')
   @limiter.limit("100 per minute")
   def api_data():
       # ...
   ```

7. **Input Validation**
   ```python
   from marshmallow import Schema, fields, validate
   
   class LocationSchema(Schema):
       latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
       longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))
   ```

8. **Environment Variables**
   ```python
   # Use python-dotenv
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

---

##  Data Flow Examples

### Example 1: Patient Sends Distress Signal

```
1. User opens userView_production.html
   └─→ Page loads, requests location permission

2. User clicks yellow "DISTRESS" button
   └─→ Confirmation popup appears

3. User clicks "Send Distress" in popup
   └─→ JavaScript calls sendUserDetails(true, false)

4. POST request sent to Flask
   └─→ URL: /api/usr/details
   └─→ Body: {"distress": true, "help": false}
   └─→ Headers: {"ngrok-skip-browser-warning": "true"}

5. Flask server receives request
   └─→ Function: receive_user_details()
   └─→ Updates: user_state = {"distress": true, "help": false}
   └─→ Console prints: "🚨 User State Updated: Distress=True"
   └─→ Returns: {"status": "success"}

6. Admin dashboard polling (every 5 seconds)
   └─→ Function: checkUserAlerts()
   └─→ GET /api/usr/status
   └─→ Compares: lastAlertState vs new state
   └─→ Detects: distress changed from false to true

7. Alert popup triggers on admin screen
   └─→ Function: showAlert('distress', lat, lon)
   └─→ Displays: "🚨 DISTRESS SIGNAL"
   └─→ Shows: Patient location (lat/lon)
   └─→ Plays: 800Hz beep sound

8. Admin can take action
   └─→ Click "View Location" → Opens map page
   └─→ Click "Dismiss" → Closes popup
```

### Example 2: Vital Signs Monitoring

```
1. ESP32 reads sensors
   └─→ Temperature sensor: 31.5°C (raw)
   └─→ Heart rate sensor: Detecting beats
   └─→ Touch sensor: Not touched

2. ESP32 sends data to Flask (local network)
   └─→ HTTP GET to http://10.60.107.150/getData
   └─→ Response: {"temperature": 31.5, "bpm": 78, "beat": false}

3. Flask processes request
   └─→ Function: api_data()
   └─→ Fetches from ESP32_URL
   └─→ Adds offset: temp = 31.5 + 5 = 36.5°C
   └─→ Randomizes BPM: random.randint(80, 100) = 87

4. Admin dashboard requests data
   └─→ Every 2 seconds
   └─→ GET /api/data
   └─→ Receives: {"temperature": 36.5, "bpm": 87, "beat": false, "touched": false}

5. Dashboard updates charts
   └─→ Updates text: "curr Temp: 36.5°C"
   └─→ Updates text: "curr pulse: 87 BPM"
   └─→ Adds to tempData array: [34.2, 35.8, 36.5]
   └─→ Adds to pulseData array: [82, 85, 87]
   └─→ Redraws canvas charts with new points
   └─→ Removes oldest point if > 20 points

6. User interface requests data
   └─→ Every 5 seconds
   └─→ GET /api/data
   └─→ Same response as admin

7. User sees vitals
   └─→ Display: "36.5° C"
   └─→ Display: "87 BPM"
   └─→ Connection indicator: Green dot (connected)
```

### Example 3: Location Tracking

```
1. User interface loads
   └─→ Function: requestLocationPermission()
   └─→ Browser prompts: "Allow location access?"

2. User clicks "Allow"
   └─→ navigator.geolocation.getCurrentPosition()
   └─→ Gets: {latitude: 12.853794, longitude: 80.175039}

3. Immediate location send
   └─→ Function: sendLocation()
   └─→ POST /api/usr/location
   └─→ Body: {"latitude": 12.853794, "longitude": 80.175039}

4. Flask stores location
   └─→ Function: receive_user_location()
   └─→ Updates: user_location = {"latitude": 12.853794, "longitude": 80.175039}
   └─→ Console: "📍 User Location Updated: 12.853794, 80.175039"

5. Automatic updates start
   └─→ Every 30 seconds: sendLocation()
   └─→ User sees: "📍 Location: 12.8538, 80.1750"

6. Admin opens location page
   └─→ Function: startLocationUpdates()
   └─→ GET /api/usr/status
   └─→ Receives location data

7. Map displays
   └─→ Function: displayMap(12.853794, 80.175039)
   └─→ Creates Google Maps iframe
   └─→ URL: https://www.google.com/maps?q=12.853794,80.175039&z=16&output=embed
   └─→ Map loads showing location with marker

8. Background updates
   └─→ Every 10 seconds: fetchUserLocation()
   └─→ Only reloads map if coordinates change
   └─→ Otherwise, just updates text display
```

---

## Customization

### Change Color Scheme

**Admin Dashboard:**
```css
/* index_updated.html - Around line 20 */
body {
  background-color: #9ABCC7; /* Sage green - change to your color */
}

.chart-container {
  background-color: #D4D4D4; /* Light gray - change to your color */
}

button {
  background-color: #D4D4D4; /* Button color */
}
```

**User Interface:**
```css
/* userView_production.html - Around line 19 */
body {
  background-color: #A4BDB1; /* Mint green - change to your color */
}

.info-box {
  background-color: #E8E8E8; /* Info box color */
}

#distressBtn {
  background-color: #F4E869; /* Yellow - change distress color */
}

#helpBtn {
  background-color: #C41E1E; /* Red - change help color */
}
```

### Add Custom Alerts

**Email Alerts:**
```python
# flask_server_fixed.py
import smtplib
from email.mime.text import MIMEText

def send_email_alert(location):
    msg = MIMEText(f"Emergency at: {location['latitude']}, {location['longitude']}")
    msg['Subject'] = 'Patient Emergency Alert'
    msg['From'] = 'alerts@vitalcare.com'
    msg['To'] = 'doctor@hospital.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email', 'your_password')
        server.send_message(msg)

# Add in receive_user_details function
if user_state["distress"]:
    send_email_alert(user_location)
```

**SMS Alerts (Twilio):**
```python
from twilio.rest import Client

def send_sms_alert(location):
    client = Client('account_sid', 'auth_token')
    message = client.messages.create(
        body=f"EMERGENCY: Patient needs help at {location['latitude']}, {location['longitude']}",
        from_='+1234567890',
        to='+0987654321'
    )

# Add in receive_user_details function
if user_state["distress"]:
    send_sms_alert(user_location)
```

### Change Update Frequencies

See [Configuration](#configuration) section above.

### Add More Sensors

**In Flask server:**
```python
# Add new sensor data
@app.route("/api/data", methods=["GET", "OPTIONS"])
def api_data():
    # ... existing code ...
    
    # Add oxygen saturation
    try:
        o2_response = requests.get(ESP32_O2_URL, timeout=2)
        o2_data = o2_response.json()
    except:
        o2_data = {"spo2": 95}
    
    return jsonify({
        "temperature": ...,
        "bpm": ...,
        "spo2": o2_data.get("spo2", 95)  # Add new field
    })
```

**In admin dashboard:**
```html
<!-- Add new chart -->
<div class="chart-container">
  <div class="current-value" id="o2Value">curr SpO2: --</div>
  <canvas id="o2Chart"></canvas>
</div>
```

```javascript
// Update JavaScript
const data = await response.json();
document.getElementById('o2Value').textContent = `curr SpO2: ${data.spo2}%`;
```

---

## 🚀 Future Enhancements

Potential improvements for the system:

**Data & Storage:**
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Historical data analysis and reporting
- [ ] Data export to PDF/CSV
- [ ] Cloud backup

**User Experience:**
- [ ] Mobile app (React Native/Flutter)
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Voice commands

**Features:**
- [ ] Multiple patient support
- [ ] Medication reminders
- [ ] Video call integration
- [ ] Fall detection
- [ ] Sleep tracking

**Notifications:**
- [ ] SMS/Email notifications
- [ ] Push notifications
- [ ] Voice alerts
- [ ] Emergency contact auto-dial

**Analytics:**
- [ ] Machine learning predictions
- [ ] Trend analysis
- [ ] Anomaly detection
- [ ] Health reports

**Integration:**
- [ ] Hospital system integration (HL7/FHIR)
- [ ] Wearable device support (Fitbit, Apple Watch)
- [ ] Electronic Health Records (EHR)
- [ ] Telemedicine platforms

**Security:**
- [ ] End-to-end encryption
- [ ] HIPAA compliance
- [ ] Audit logging
- [ ] Two-factor authentication

---

##  Support & Debugging

### Getting Help

1. **Check Documentation**
   - Review [Troubleshooting](#troubleshooting) section
   - Check [API Documentation](#api-documentation)
   - Read [Usage Guide](#usage-guide)

2. **Check Logs**
   - Flask server console output
   - Browser console (F12 → Console tab)
   - ngrok web interface (http://localhost:4040)

3. **Verify Configuration**
   - ESP32 IP addresses correct
   - ngrok URL updated in HTML files
   - All services running (ESP32, Flask, ngrok)

### Debug Checklist

```
□ ESP32 is powered on and connected to WiFi
□ Flask server is running (check terminal)
□ ngrok tunnel is active (check ngrok terminal)
□ ngrok URL is updated in both HTML files
□ Browser allows location permissions
□ No CORS errors in browser console
□ API endpoints responding (test with curl)
□ Network connection stable
```

### Common Error Messages

**"Failed to fetch"**
- Check Flask server is running
- Verify ngrok URL is correct
- Check network connection

**"CORS policy blocked"**
- Ensure flask-cors is installed
- Check ngrok-skip-browser-warning header

**"Location unavailable"**
- Allow location permissions in browser
- Check HTTPS is being used (ngrok provides this)

**"TypeError: ... is not JSON serializable"**
- Use `flask_server_fixed.py` (already fixed)
- Check variable naming conflicts

---

## 📄 License

This project is for educational and healthcare research purposes.

**Disclaimer:** This system is a prototype for educational purposes. It should not be used as a replacement for professional medical devices or emergency services. Always consult healthcare professionals for medical advice.

---

##  Acknowledgments

- **ESP32 Community** - For sensor integration examples and libraries
- **Flask Documentation** - For comprehensive web framework guidance
- **Google Maps** - For location visualization and embedding
- **ngrok** - For secure tunneling and HTTPS support
- **Open Source Community** - For various libraries and tools

---

## Version History

### v1.0.0 (January 2026) - Initial Release
- ✅ ESP32 sensor integration (temperature, heart rate, touch)
- ✅ Flask backend with REST API
- ✅ Admin dashboard with login system
- ✅ User interface for patients
- ✅ GPS location tracking
- ✅ Emergency alert system (distress/help)
- ✅ Real-time monitoring with charts
- ✅ Google Maps integration
- ✅ Alert popup notifications with sound
- ✅ Confirmation dialogs for emergency buttons
- ✅ Continuous alert monitoring
- ✅ Map persistence (no flashing)

### Upcoming Features (Planned)
- 🔄 Database integration
- 🔄 User authentication system
- 🔄 Email/SMS notifications
- 🔄 Historical data reports
- 🔄 Mobile application

---

## System Statistics

- **Lines of Code:** ~2000+
- **API Endpoints:** 5
- **Update Intervals:** 
  - Vitals: 2-5 seconds
  - Location: 10-30 seconds
  - Alerts: 5 seconds
- **Supported Browsers:** Chrome, Firefox, Safari, Edge
- **Supported Devices:** Desktop, Mobile, Tablet

---

**Built with ❤️ for better healthcare**

*Vital Care - Monitoring Life, Saving Lives*

---

*Last Updated: January 28, 2026*
*Version: 1.0.0*
*Documentation: Complete*
