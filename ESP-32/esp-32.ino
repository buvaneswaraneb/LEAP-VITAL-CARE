#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

/* ================= WIFI ================= */
const char* ssid = "Moto";
const char* password = "cocomelon";


/* ============== PIN DEFINITIONS ============== */
#define PULSE_SENSOR_PIN 13
#define DS18B20_PIN 14
#define TOUCH_PIN 15

/* ============== PULSE VARIABLES ============== */
#define THRESHOLD 2000
int BPM = 0;
int signalValue = 0;
int lastSignalValue = 0;
unsigned long lastBeatTime = 0;
bool beatDetected = false;
bool touchDetected = false;
unsigned long lastTouchTime = 0;


/* ============== TEMP SENSOR ============== */
OneWire oneWire(DS18B20_PIN);
DallasTemperature sensors(&oneWire);
float bodyTemp = 0.0;
unsigned long lastTempRead = 0;
const unsigned long TEMP_INTERVAL = 2000;

/* ============== TOUCH ============== */
bool lastTouchState = LOW;

/* ============== SERVER ============== */
WebServer server(80);

/* ================= SETUP ================= */
void setup() {
  Serial.begin(115200);

  pinMode(TOUCH_PIN, INPUT);
  sensors.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/getData", HTTP_GET, handleGetData);
  server.on("/getTouch", HTTP_GET, handleGetTouch);
  server.begin();

  Serial.println("Web server started");
}

/* ================= LOOP ================= */
void loop() {
  server.handleClient();
  readPulse();
  readTemperature();
  checkTouch();
}

/* ================= PULSE ================= */
void readPulse() {
  signalValue = analogRead(PULSE_SENSOR_PIN);

  if (signalValue > THRESHOLD && lastSignalValue <= THRESHOLD) {
    unsigned long now = millis();
    if (lastBeatTime > 0) {
      unsigned long diff = now - lastBeatTime;
      if (diff > 300 && diff < 2000) {
        BPM = 60000 / diff;
      }
    }
    lastBeatTime = now;
    beatDetected = true;
  } else {
    beatDetected = false;
  }

  lastSignalValue = signalValue;
}

/* ================= TEMP ================= */
void readTemperature() {
  if (millis() - lastTempRead >= TEMP_INTERVAL) {
    sensors.requestTemperatures();
    bodyTemp = sensors.getTempCByIndex(0);
    lastTempRead = millis();
  }
}

/* ================= TOUCH ================= */
void checkTouch() {
  bool touchState = digitalRead(TOUCH_PIN);

  if (touchState == HIGH && lastTouchState == LOW) {
    Serial.println("🚨 TOUCH DETECTED");
    touchDetected = true;
    lastTouchTime = millis();
  }

  lastTouchState = touchState;

  // auto reset after 2 seconds
  if (touchDetected && millis() - lastTouchTime > 2000) {
    touchDetected = false;
  }
}


/* ================= FLASK POST ================= */
void sendTouchToFlask() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.setTimeout(2000);   // safety
    http.begin(flaskURL);
    http.addHeader("Content-Type", "application/json");

    String json = "{";
    json += "\"touched\":true,";
    json += "\"temperature\":" + String(bodyTemp, 2) + ",";
    json += "\"bpm\":" + String(BPM);
    json += "}";

    int code = http.POST(json);
    Serial.print("Flask response: ");
    Serial.println(code);

    http.end();
  }
}
void handleGetTouch() {
  String json = "{";
  json += "\"touched\":" + String(touchDetected ? "true" : "false");
  json += "}";

  server.send(200, "application/json", json);
}

/* ================= WEB PAGE ================= */
void handleRoot() {
  String html = "<h1>ESP32 Health Monitor</h1>";
  html += "<p>Temperature: " + String(bodyTemp) + " C</p>";
  html += "<p>BPM: " + String(BPM) + "</p>";
  server.send(200, "text/html", html);
}

/* ================= JSON API ================= */
void handleGetData() {
  String json = "{";
  json += "\"temperature\":" + String(bodyTemp, 2) + ",";
  json += "\"bpm\":" + String(BPM) + ",";
  json += "\"beat\":" + String(beatDetected ? "true" : "false");
  json += "}";

  server.send(200, "application/json", json);

}
