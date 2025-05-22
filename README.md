# 🛠️ SolarBoat Framework

This repository contains the **Autonomous Ship Control Framework**, a modular system designed to seamlessly connect and manage dedicated sensors, the CAN bus, actuators, communication modules (e.g., 4G), GPS, and a decision-making module. This framework acts as the backbone for orchestrating autonomous ship operations in real-world and simulated environments.


![image](https://github.com/user-attachments/assets/49beafc7-d98f-45ee-9129-125b8b236b02)

---

## 🌟 Core Objectives

### Version 0:
- [ ] **CAN Bus Management**:
  - Handle communication between actuators and end devices on the CAN bus.
- [ ] **Sensor Integration**:
  - Connect and test sensors.
- [ ] **Decision-Making Module**:
  - Orchestrates autonomous navigation and control of the vehicle.
- [ ] **Communication Channels**:
  - Enable communication via 4G for real-time data transfer.

> [!WARNING]
> 4G is notoriously unstable near borders. Take extra care.

---

## 🛣️ Roadmap

### 🚀 Upcoming Features:
- [ ] **Modular Sensor Drivers**:
  - Add drivers for more specialized sensors and dynamic configuration.
- [ ] **4G Redundancy**:
  - Introduce failover mechanisms for robust communication.
- [ ] **GPS Data Enrichment**:
  - Fuse GPS data with additional telemetry for better localization.
- [ ] **Simulation Support**:
  - Create hooks for Unreal Engine or other simulators to test the framework.

---

## 📦 Features

- 🔌 **Sensor Integration**:
  - Support for various dedicated sensors (e.g., LiDAR, cameras, depth sensors).
- 📡 **CAN Bus Communication**:
  - Robust messaging between devices, including actuators and controllers.
- 🌍 **GPS Support**:
  - Real-time positioning with logging and analysis.
- 📶 **4G Communication**:
  - Enable remote data transfer and decision relays.
- 🧠 **Decision-Making Module**:
  - A pluggable interface for integrating autonomous control logic.

---

## 📋 Project Structure

```plaintext
📂 SolarBoatFrame
├── 4g                  # (Unimplemented) 4G networking interface
├── can_bus             # High level CAN interface and manager
├── documentation       # Any documentation regarding the Project
├── gps_coordinate      # Coordinate representation classes
│   └── geofence        # Geofence implementation
├── logging             # All logfiles
├── ship_state          # Current ship state and ship properties
├── tests               # All unit tests for the Project
└── README.md           # This document
```

---

## Setup

You need root privileges for the setupper.

1. Make the setup bash script executable:
      ```bash
      sudo chmod +x setup_env.sh
      ```

2. python main.py is the entry point.

---

## Testing

From the root, use this command in terminal:


  ```python
  pytest tests/
  ```

---

## Gists & snippets

[Python basic GPS using geopy and geocoder](https://gist.github.com/LordLokator/e056aad11b58d2d68011c2a2d5450408)


---

## 👥 Team & Contributors
[**BME SolarBoat Team**](https://solarboatteam.hu/)
