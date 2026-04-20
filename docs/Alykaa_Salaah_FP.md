---
marp: true
theme: default
paginate: true
---

# 🌱 Smart Plant Monitor  
### Alykaa Salaah  
CSC 494 • Final Presentation

---

# The Problem

- People forget to water their plants  
- Sometimes plants get too much or too little water  
- There’s no simple way to monitor plant health in real time  

---

# The Solution

- Build an IoT plant monitoring system  
- Track:
  - Soil moisture  
  - Temperature  
  - Humidity  
- Send data wirelessly to a dashboard  
- Show plant health in real time  

---

# My Tools & Technology

**Hardware:**
- XIAO ESP32C6  
- Soil Moisture Sensor  
- AHT10 Sensor  
- Breadboard + wires  

**Software:**
- Arduino (C++)  
- Python (server)  
- Streamlit (dashboard)

---

# How It Works

1. Sensors collect data  
2. ESP32 reads the data  
3. Data is sent over WiFi  
4. Python server receives it  
5. Dashboard displays it live  

---

# Sprint Plan

Project is split into **two 5-week sprints**

- Sprint 1 → Build foundation  
- Sprint 2 → Add intelligence & polish  

---

# Sprint 1 – MVP & Connectivity

**Goals:**
- Set up hardware  
- Read temperature & moisture  
- Build basic dashboard (Arduino IDE)

---

# First attempt at Breadboard
![bg right:40%]([images/Failed_attempt.pdf](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/Failed%20attempt.pdf))

---

# Sprint 1 Results

- Live sensor data working  
- ESP32 successfully sending data  

Example:
- Soil Moisture: 2%  
- Temperature: 21.4°C  
- Humidity: 43%  

![bg right:40%](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/Sprint%201%20results.png)

---

# Sprint 1 board result

![bg right:40%](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/Breadboard%20Currently.pdf)

---

# Data Visualization

- Added live graphs  
- Tracks changes over time  
- Helps understand plant conditions  

---

# Sprint 2 – Intelligence & Features

**Goals:**
- Connect ESP32 to WiFi
- Python server receiving data  
- Send data to server  
- Store historical data  
- Improve dashboard UI  
- Add watering recommendations  
- Add alerts/notifications
- Dashboard showing real-time values  
- Test and polish system  

---

# Learned with AI

- Helped debug Arduino code  
- Helped connect WiFi + server  
- Helped build dashboard  
- Helped understand full system  

---

# Learning with AI:
**Topic 1:** IoT Sensor Communication (HTTP vs MQTT)

**Topic 2:** SQLite for IoT Data

---

# Dashboard visualzation picture

![bg right:40%](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/The%20Setup.png)

---

# Dashboard

- Built with Streamlit  
- Displays:
  - Soil moisture  
  - Temperature  
  - Humidity  
- Shows plant status:
  - Needs water  
  - Healthy  

---

# Dashboard Picture

![bg right:40%](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/Dashboard%20results.png)

---
# Demo (live)

- Video
- <a href="[YouTube](https://youtu.be/wB_I8LaZoao )">Youtube</a>

---
# Some Challenges
![bg right:40%](https://github.com/Salaaha2/iot-smart-plant-monitor/blob/main/docs/images/Water%20system.pdf)

---
# Some Challenges

- No Automatic Pump
- Wiring sensors correctly  
- Getting consistent sensor readings  
- WiFi connection issues  
- Connecting everything together  

---

# Future Improvements

- Add water pump automation  
- Make dashboard look more like an app  
- Add notifications  
- Deploy online  

---

# Time of Reflection

- Learned how hardware and software connect  
- Got better at debugging  
- Built a full working IoT system  

---

# 🙌🏾 Thank You

Questions?
