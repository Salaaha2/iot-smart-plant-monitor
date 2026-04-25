/*
  PlantIQ_ESP32-1 | Xiao ESP32C6
  ─────────────────────────────────────────────────loop kk
  WIRING
    Soil moisture  AOUT → D0 (A0)
    Water level    SIG  → D1 (A1)
    Pump relay     IN   → D7
    AHT10          SDA  → D4   SCL → D5

  LIBRARIES  (Tools → Manage Libraries)
    ArduinoJson  v7   by Benoit Blanchon
    Adafruit AHTX0    by Adafruit
    Adafruit Unified Sensor (installed automatically)
    WiFi / WebServer  — built-in, no install needed

  HOW IT WORKS
    ESP32 runs a tiny HTTP server on port 80.
    server.py calls GET /data every 5 s  →  gets JSON.
    server.py calls GET /pump?state=on|off  →  controls pump.
    Your code never needs to know the server's IP address.
*/

#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <ArduinoJson.h>

// WiFi credentials
#define WIFI_SSID  "..." //YOUR_WIFI_USERNAME
#define WIFI_PASS  "..."  //YOUR_WIFI_PASS

// Pins
#define SOIL_PIN   D0   // Soil moisture AOUT
#define WATER_PIN  D1   // Water level SIG
#define PUMP_PIN   D7   // Relay IN


#include <HTTPClient.h>

void sendData(int soil, float temp, float humidity) {
  HTTPClient http;

  // Replace YOUR_MAC_IP with your computer's IP address (check with ifconfig)
  http.begin("http://YOUR_MAC_IP:5000/data");   // e.g. 192.168.x.x
  http.addHeader("Content-Type", "application/json");

  String json = "{\"soil\":" + String(soil) +
                ",\"temp\":" + String(temp) +
                ",\"humidity\":" + String(humidity) + "}";

  http.POST(json);
  http.end();
}
// Soil calibration (YOUR values — keep these)
int dryValue = 2000;
int wetValue = 800;

// Water level calibration
// Measure these the same way: sensor in empty tank vs full tank
int waterEmpty = 300;
int waterFull  = 2800;

// Pump Safety
const unsigned long PUMP_MAX_MS = 30000; // auto-off after 30 s

// Globals
Adafruit_AHTX0 aht;
bool           ahtOk = false;

float soilPct      = 0;
float waterPct     = 0;
float tempC        = 0;
float humPct       = 0;
bool  pumpOn       = false;
unsigned long pumpStartMs = 0;

unsigned long lastRead = 0;
const unsigned long READ_INTERVAL = 2000;


// Pump helpers
void setPump(bool on) {
  pumpOn = on;
  digitalWrite(PUMP_PIN, on ? HIGH : LOW);
  if (on) pumpStartMs = millis();
  Serial.println(on ? "[Pump] ON" : "[Pump] OFF");
}

// Read all sensors
void readSensors() {
  // Soil moisture (your original logic — kept exactly)
  int soilRaw = analogRead(SOIL_PIN);
  soilPct = map(soilRaw, dryValue, wetValue, 0, 100);
  soilPct = constrain(soilPct, 0, 100);

  // Water level — same pattern as soil  (Issue 3 fix)
  int waterRaw = analogRead(WATER_PIN);
  waterPct = map(waterRaw, waterEmpty, waterFull, 0, 100);
  waterPct = constrain(waterPct, 0, 100);

  // AHT10
  if (ahtOk) {
    sensors_event_t humidity, temp;
    aht.getEvent(&humidity, &temp);
    tempC  = temp.temperature;
    humPct = humidity.relative_humidity;
  }

  Serial.printf("[Sensors] Soil:%.1f%%  Water:%.1f%%  Temp:%.1fC  Hum:%.1f%%\n",
                soilPct, waterPct, tempC, humPct);
}


// Setup
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== PlantIQ ESP32C6 – Sprint 2 ===");

  // ADC
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  pinMode(SOIL_PIN,  INPUT);
  pinMode(WATER_PIN, INPUT);
  pinMode(PUMP_PIN,  OUTPUT);
  // Pump not connected yet (simulation only)
  digitalWrite(PUMP_PIN, LOW);   // pump OFF at startup

  // AHT10
  Wire.begin();
  ahtOk = aht.begin();
  Serial.println(ahtOk ? "[AHT10] Found" : "[AHT10] NOT found – check wiring");

  // Initial sensor read
  readSensors();

  // WiFi
  Serial.printf("[WiFi] Connecting to %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    if (++tries > 30) {
      Serial.println("\n[WiFi] Failed – check credentials");
      while (true) delay(1000);
    }
  }
  Serial.println("\n[WiFi] Connected!");
  Serial.print("[WiFi] IP: ");
  Serial.print("[WiFi] IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("\n  ★ Paste this IP into server.py → ESP32_IP ★\n");
  Serial.println("System Ready\n");
}

// Loop
void loop() {

  // Read soil
  int soilRaw = analogRead(SOIL_PIN);
  int soilPercent = map(soilRaw, dryValue, wetValue, 0, 100);
  soilPercent = constrain(soilPercent, 0, 100);

  // Read temp + humidity
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  // Print (for debugging)
  Serial.println("------");
  Serial.print("Soil: "); Serial.print(soilPercent); Serial.println("%");
  Serial.print("Temp: "); Serial.print(temp.temperature); Serial.println(" C");
  Serial.print("Humidity: "); Serial.print(humidity.relative_humidity); Serial.println("%");

  // SEND DATA (put it HERE)
  sendData(soilPercent, temp.temperature, humidity.relative_humidity);

  delay(5000);
}