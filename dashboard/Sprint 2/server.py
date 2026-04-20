from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

DB_FILE = "plantiq.db"

# Database setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            soil        INTEGER,
            temperature REAL,
            humidity    REAL
        )
    """)
    # Plant health log — written every time status changes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS health_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            status    TEXT,
            soil      INTEGER,
            message   TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_status(soil):
    """Return (status_label, message) based on soil moisture."""
    if soil < 30:
        return "Needs Water", "Soil is too dry — plant needs water now."
    elif soil < 60:
        return "Getting Dry", "Soil moisture is low — consider watering soon."
    elif soil <= 85:
        return "Healthy", "Soil moisture is at a great level."
    else:
        return "Overwatered", "Soil is too wet — skip watering for now."

# Receive data from ESP32 (POST /data)
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    soil     = data.get('soil')
    temp     = data.get('temp')
    humidity = data.get('humidity')
    now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nReceived  Soil:{soil}%  Temp:{temp}°C  Hum:{humidity}%")

    conn = sqlite3.connect(DB_FILE)

    # Save sensor reading
    conn.execute("""
        INSERT INTO sensor_data (timestamp, soil, temperature, humidity)
        VALUES (?, ?, ?, ?)
    """, (now, soil, temp, humidity))

    # Save to health log only when status changes
    status, message = get_status(soil)
    last = conn.execute("""
        SELECT status FROM health_log ORDER BY id DESC LIMIT 1
    """).fetchone()

    if not last or last[0] != status:
        conn.execute("""
            INSERT INTO health_log (timestamp, status, soil, message)
            VALUES (?, ?, ?, ?)
        """, (now, status, soil, message))
        print(f"   Status changed → {status}")

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# Get latest + recent readings (GET /data)
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("""
        SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50
    """).fetchall()
    conn.close()
    return jsonify(rows)

# Get health log (GET /history)
@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("""
        SELECT * FROM health_log ORDER BY id DESC LIMIT 30
    """).fetchall()
    conn.close()
    return jsonify(rows)

# Get daily stats (GET /stats)
@app.route('/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("""
        SELECT
            ROUND(AVG(soil), 1)        as avg_soil,
            MIN(soil)                   as min_soil,
            MAX(soil)                   as max_soil,
            ROUND(AVG(temperature), 1) as avg_temp,
            ROUND(AVG(humidity), 1)    as avg_hum,
            COUNT(*)                   as total_readings
        FROM sensor_data
        WHERE timestamp >= date('now')
    """).fetchone()
    conn.close()
    return jsonify({
        "avg_soil":        row[0] or 0,
        "min_soil":        row[1] or 0,
        "max_soil":        row[2] or 0,
        "avg_temp":        row[3] or 0,
        "avg_hum":         row[4] or 0,
        "total_readings":  row[5] or 0,
    })

# Main
if __name__ == '__main__':
    init_db()
    print("🚀 PlantIQ server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
