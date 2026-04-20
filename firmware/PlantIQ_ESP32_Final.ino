/*
  PlantIQ – Xiao ESP32C6
  Posts sensor data to Python server every 5 seconds

  WIRING:
    Soil sensor  AOUT → D0
    AHT10        SDA  → D4   SCL → D5
    (No pump in this version)

  LIBRARIES (Tools → Manage Libraries):
    Adafruit AHTX0 + Adafruit Unified Sensor
    ArduinoJson v7
    WiFi + HTTPClient — built in
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <ArduinoJson.h>

// ── WiFi ──────────────────────────────────────────────────────
#define WIFI_SSID  "TwinS"
#define WIFI_PASS  "October1"

// ── Server  (your Mac's IP shown in server.py output) ─────────
#define SERVER_IP  "192.168.1.247"   // ← your Mac's IP
#define SERVER_URL "http://" SERVER_IP ":5000/data"

// ── Pins ──────────────────────────────────────────────────────
#define SOIL_PIN  D0

// ── Calibration (your values) ─────────────────────────────────
int dryValue = 2000;
int wetValue  = 800;

// ── Globals ───────────────────────────────────────────────────
Adafruit_AHTX0 aht;
bool ahtOk = false;

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("[WiFi] Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n[WiFi] Connected!");
  Serial.print("[WiFi] ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void sendData(int soil, float temp, float humidity) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WiFi] Reconnecting...");
    connectWiFi();
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  // Build JSON
  JsonDocument doc;
  doc["soil"]     = soil;
  doc["temp"]     = round(temp * 10) / 10.0;
  doc["humidity"] = round(humidity * 10) / 10.0;
  String json;
  serializeJson(doc, json);

  int code = http.POST(json);
  if (code == 200) {
    Serial.println("[HTTP] Data sent ✓");
  } else {
    Serial.print("[HTTP] Failed, code: ");
    Serial.println(code);
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== PlantIQ ESP32C6 ===");

  // ADC setup
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  pinMode(SOIL_PIN, INPUT);

  // AHT10
  Wire.begin();
  ahtOk = aht.begin();
  Serial.println(ahtOk ? "[AHT10] Found ✓" : "[AHT10] Not found – check wiring");

  connectWiFi();
  Serial.println("System Ready\n");
}

void loop() {
  // Read soil moisture
  int soilRaw = analogRead(SOIL_PIN);
  int soil    = map(soilRaw, dryValue, wetValue, 0, 100);
  soil        = constrain(soil, 0, 100);

  // Read AHT10
  float temp = 0, humidity = 0;
  if (ahtOk) {
    sensors_event_t hum_ev, temp_ev;
    aht.getEvent(&hum_ev, &temp_ev);
    temp     = temp_ev.temperature;
    humidity = hum_ev.relative_humidity;
  }

  // Print to Serial
  Serial.println("──────────────────────");
  Serial.print("Soil:     "); Serial.print(soil);     Serial.println("%");
  Serial.print("Temp:     "); Serial.print(temp);     Serial.println("°C");
  Serial.print("Humidity: "); Serial.print(humidity); Serial.println("%");

  // Send to server
  sendData(soil, temp, humidity);

  delay(5000);  // send every 5 seconds
}
