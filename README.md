# 🛠️ SolarBoat Framework

This repository contains the **Autonomous Ship Control Framework**, a modular system designed to seamlessly connect and manage dedicated sensors, the CAN bus, actuators, communication modules (e.g., 4G), GPS, and a decision-making module. This framework acts as the backbone for orchestrating autonomous ship operations in real-world and simulated environments.

We based our implementation on the work [[1]](#1) of Tomera M. and Alfuth Ł.


![image](https://github.com/user-attachments/assets/49beafc7-d98f-45ee-9129-125b8b236b02)

---

## 🌟 Core Objectives
### Version 0:
- [x] **Ship Coordinate System & Navigation Math**
  - Convert GPS coordinates to Earth/body-fixed frames.
  - Compute heading and cross-track errors (Eq. 4, 41, 46).
- [x] **GPS Integration**
  - Real-time GPS tracking with NED offsets and geofence safety.
- [x] **Waypoint Navigation Controller**
  - PDPI control algorithm as described in [1].
- [x] **ShipPosition Class**
  - Centralized source for position, heading, velocity vectors (`eta`, `nu`, `U`).
- [x] **Threaded GPS Update Loop**
  - Background polling for position updates.
- [x] **Clean CANManager Interface**
  - Message receiving via background thread and `read_state()` access.
- [x] **Modular Architecture (ShipState / ShipTaskManager)**
  - Separates state handling from control logic.

> [!WARNING]
> 4G is notoriously unstable near borders. Take extra care.

---

## 🛣️ Roadmap

### 🔄 In Progress
- [ ] **Route Management in ShipState**
  - Automatic segment switching and waypoint arrival logic.
- [ ] **ShipTaskManager Control Loop**
  - Generate rudder/engine commands via PDPI based on state.
- [ ] **CAN Protocol Finalization**
  - Implement exact message layout for incoming/outgoing data.

### 🚀 Upcoming Features:
- [ ] **Path History Logging**
  - Store past position, heading, and error metrics.
- [ ] **Testing & Replay Tools**
  - Replay logs for testing controller behavior.
- [ ] **Simulated GPS / CAN Sources**
  - Offline testing with mocked hardware input.
- [ ] **Web UI or CLI Dashboard**
  - Real-time monitoring and override tools.

---

## 📦 Features

- 🔌 **Sensor Integration**
  - Support for GPS and CAN-fed ship metrics (u, v, r).
- 📡 **CAN Bus Communication**
  - Bidirectional messaging with actuators and state publishers.
- 🧭 **Waypoint Controller**
  - Real-time rudder angle and surge speed computation.
- 🌍 **Geofencing**
  - Ensure test or race operation stays in safe bounds.
- 🧠 **Modular Task Management**
  - Decoupled design allows easy testing and component replacement.

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


To create a file 'tree.txt' with the project layout, use this command in the project root:

```
tree -I 'documentation|__pycache__|tests|tree.txt' --noreport > tree.txt
```


---

## 👥 Team & Contributors
[**BME SolarBoat Team**](https://solarboatteam.hu/)


## References

<a id="1">[1]</a>
Tomera M., Alfuth Ł. (June 2020).
Waypoint Path Controller for Ships. [**[link]**](https://www.transnav.eu/Article_Waypoint_Path_Controller_for_Ships_Tomera,54,1014.html) \
TransNav, the International Journal on Marine Navigation and Safety of Sea Transportation, Vol. 14, No. 2, doi:10.12716/1001.14.02.14, pp. 375-383, 2020