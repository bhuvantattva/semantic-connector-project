🏠 Smart Home Semantic Connector & Orion-LD Integration

## 📌 Overview

This project implements a **Semantic Connector pipeline** to standardize smart home IoT data and integrate it into **FIWARE Orion-LD** using NGSI-LD.

The system converts raw device data into a structured format, enabling interoperability and real-time visualization.

---

## 🚨 Problem Statement

Smart home devices generate data in inconsistent formats:

* Different units and structures
* No common schema
* Difficult integration

### Examples

* Temperature → `"22°C"`
* Power → `"2300W"`

---

## 🎯 Objective

* Standardize IoT device data
* Convert raw data into NGSI-LD entities
* Integrate with Orion-LD
* Enable real-time visualization

---

## 🏗️ Architecture

```
IoT Devices
   ↓
MySQL (Raw Data)
   ↓
Semantic Connector (Python)
   ↓
MySQL (Processed Data)
   ↓
Orion-LD (Docker + MongoDB)
   ↓
Streamlit Dashboard
```

---

## ⚙️ Tech Stack

* Python
* MySQL
* MongoDB (Docker)
* FIWARE Orion-LD (Docker)
* NGSI-LD
* Streamlit

---

## 🐳 Docker Services

* MongoDB (backend database for Orion-LD)
* Orion-LD (context broker)

---

## 📂 Project Structure

```
semantic-connector-project/
├── app.py
├── semantic_connector.py
├── delete_entities.py
├── docker-compose.yml
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── database/
│   └── schema.sql
└── sample_data/
    └── raw_data.sql
```

---

## 🧠 Core Components

### Raw Data Table

```sql
CREATE TABLE raw_device_data_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    device_type VARCHAR(50),
    raw_payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Processed Data Table

```sql
CREATE TABLE processed_device_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id VARCHAR(100),
    entity_type VARCHAR(50),
    attribute_name VARCHAR(50),
    attribute_value VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Semantic Connector

* Reads raw JSON data
* Converts to NGSI-LD format
* Sends data to Orion-LD

Example:

```python
entity = {
    "id": f"urn:ngsi-ld:{row['device_type']}:{row['device_id']}",
    "type": row['device_type'],
    "@context": [
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

---

### Orion-LD

* Stores NGSI-LD entities
* Uses MongoDB internally
* Provides REST API access

---

### Streamlit Dashboard

* Device selection
* Data table view
* Charts (Power, Temperature)
* KPI metrics

---

## 🔄 Pipeline Modes

### Mode 1

```
Raw → Transform → Store → Orion
```

### Mode 2

```
Processed → Rebuild → Orion
```

Controlled using:

```python
USE_PROCESSED_AS_SOURCE = True
```

---

## 📊 Supported Devices

* Smart Meter
* Thermostat
* EV Charger
* Solar Inverter
* Smart Light
* Door Lock
* Camera
* Humidity Sensor

---

## ⚠️ Issues Handled

### Port Conflict (MySQL)

* Cause: Port 3306 already in use
* Fix: Stop existing service or change port

---

### Data Type Issues

* Cause: Mixed values like `"22°C"`
* Fix: Convert to numeric

```python
pd.to_numeric(..., errors="coerce")
```

---

## 🔥 Features

* NGSI-LD data standardization
* Orion-LD integration
* Lightweight Docker setup
* Real-time dashboard

---
