---
marp: true
theme: default
paginate: true
size: 16:9
---

# IoT Smart Plant Environment Monitoring System
### PPP – Project Proposal Presentation
Alykaa Salaah
CSC 494

---

# Problem

Many people overwater or underwater plants  
because they don't know the real soil or environmental conditions.

Current solutions:
- guessing
- fixed timers
- manual checks

These methods are inaccurate and inefficient.

---

# Solution

Build an **IoT sensor system** that:

- measures temperature
- measures humidity
- measures soil moisture
- sends data wirelessly
- provides watering recommendations

Goal: smarter, data-driven plant care

---

# System Architecture

Sensors  
↓  
Arduino (data collection)  
↓ Serial  
ESP32 (WiFi gateway)  
↓  
Server + Dashboard  
↓  
Alerts & recommendations

---

# Hardware Components

Provided kit:
- Arduino Nano
- ESP32 (WiFi/BLE)
- Breadboard + jumper wires
- Environmental sensors

Additional (optional):
- Capacitive soil moisture sensor
- Water pump + relay, but manual alerts should be enough...

---

# Core Features

MVP:
- Read sensor data

Next:
- WiFi transmission
- Data storage
- Dashboard graphs

Final:
- watering recommendations
- alerts
- optional automation

---

# Learning with AI

## Software Topic
Data analysis & visualization
- processing sensor data
- dashboards
- trends

## Hardware Topic
ESP32 & IoT communication
- sensors
- I2C/Serial
- WiFi/MQTT

AI helps with:
- explanations
- debugging
- code examples

---

# Sprint Plan

Project projected timeline (subjected to change 🤷🏾‍♀️)

Sprint 1 → Build foundation  
Sprint 2 → Add intelligence & polish

---

# Sprint 1 – MVP & Connectivity

Goals:
- set up hardware
- read temperature & moisture
- connect ESP32 WiFi
- send data to computer/server
- basic dashboard

Deliverable:
live sensor readings online

---

# Sprint 2 – Intelligence & Features

Goals:
- store historical data
- visualize graphs
- watering recommendations
- alerts/notifications
- testing & polish

Deliverable:
smart monitoring system with insights

---

# Expected Outcomes

By the end of the semester I will have:

- working IoT device
- wireless data pipeline
- dashboard visualization
- real-time monitoring
- hands-on IoT + full-stack experience

---

# Thank You
