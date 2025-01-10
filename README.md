# 🛠️ SolarBoat Framework

This repository contains the **Autonomous Ship Control Framework**, a modular system designed to seamlessly connect and manage dedicated sensors, the CAN bus, actuators, communication modules (e.g., 4G), GPS, and a decision-making module. This framework acts as the backbone for orchestrating autonomous ship operations in real-world and simulated environments.

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
├── 📁 logging           # Logging entire framework
│   ├── logs.csv
│   └── logger.py
├── 📁 can_bus           # CAN communication logic
│   ├── can_manager.py
│   └── device_drivers/
├── 📁 communication     # 4G and data relay modules
│   └── whatever.py
├── 📁 decision_module   # Integration with decision-making logic
│   ├── top_level_interface.py
│   └── algorithms/
├── 📂 tests             # Unit and integration tests
├── 📂 documentation     # docs
└── README.md            # Project documentation
```


---

## 👥 Team & Contributors
[**BME SolarBoat Team**](https://solarboatteam.hu/)
