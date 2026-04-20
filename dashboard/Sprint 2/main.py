import requests
import time

URL = "http://localhost:5000/data"

while True:
    data = requests.get(URL).json()

    if data:
        latest = data[0]

        soil = latest[2]
        temp = latest[3]
        humidity = latest[4]

        print("\n🌱 Plant Dashboard")
        print("----------------------")
        print(f"Soil Moisture: {soil}%")
        print(f"Temperature: {temp} C")
        print(f"Humidity: {humidity}%")

        if soil < 30:
            print("⚠️ Plant Needs Water!")
        else:
            print("✅ Plant is Healthy")

    time.sleep(5)