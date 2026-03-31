🏠 Smart Home Semantic Connector & Orion-LD Integration

## Overview

This project demonstrates a **Semantic Connector** that transforms heterogeneous smart home device data into a standardized format using **NGSI-LD** and publishes it to a **FIWARE Orion-LD Context Broker**.

The system integrates:

* MySQL (raw + processed data)
* Python (data transformation & semantic mapping)
* Orion-LD (context broker)
* MongoDB (backend for Orion)
* Streamlit (dashboard visualization)

---

## Architecture

```text
MySQL (Raw Data)
        ↓
Semantic Connector (Python)
        ↓
NGSI-LD Entities
        ↓
Orion-LD (Docker)
        ↓
Streamlit Dashboard
```

---

## Project Structure

```text
semantic-connector-project/
│
├── app.py
├── semantic_connector.py
├── delete_entities.py
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── database/
│   └── schema.sql
│
├── sample_data/
│   └── raw_data.sql
│
├── .env.example
├── .gitignore
```

---

## Technology Choices

### Dataspace / Platform

* FIWARE Orion-LD

### Ontology

* **SAREF (Smart Applications REFerence ontology)**
* EU-compliant and suitable for smart energy systems

---

## What is an Ontology?

An ontology defines a **standard structure and meaning of data**.

Example:

* Different devices → "temp", "temperature"
* Standardized → `temperature` with unit `°C`

---

## Requirements

### Software

* Python 3.10+
* Docker Desktop
* MySQL Server
* (Optional) MySQL Workbench

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create `.env` from `.env.example`:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=smart_home

ORION_URL=http://localhost:1026
```

---

## Setup Instructions

### 1. Clone Repo

```bash
git clone <repo-url>
cd semantic-connector-project
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Start Docker (MongoDB + Orion)

```bash
docker compose up -d

Check running containers:
docker ps

```

---

### 4. Setup MySQL

Run schema:

```sql
SOURCE database/schema.sql;
```

Insert data:

```sql
SOURCE sample_data/raw_data.sql;
```

---

## ⚠️ IMPORTANT: Pipeline Mode (Very Important)

Your pipeline has two modes controlled by:

```python
USE_PROCESSED_AS_SOURCE = False
```

### First Run (MANDATORY)

Set:

```python
USE_PROCESSED_AS_SOURCE = False
```

### Why?

* `processed_device_data` table is initially EMPTY
* If set to True → no data will be processed
* Result → Orion empty → dashboard blank

---

### After First Run

You can switch to:

```python
USE_PROCESSED_AS_SOURCE = True
```

### Why?

* Uses already processed data
* Faster execution
* Avoids reprocessing raw data

---

### Summary

```text
First run → False
Later runs → True
```

---

## Run the Project

## How to Run the Project

### 1. Install dependencies
pip install -r requirements.txt

### 2. Start Docker services
docker compose up -d

### 3. Setup MySQL
Run:
SOURCE database/schema.sql;
SOURCE sample_data/raw_data.sql;

---

## First Run (MANDATORY)

### 4. First run configuration
Set:
USE_PROCESSED_AS_SOURCE = False

### 5. Run semantic connector
python semantic_connector.py

👉 This will:
- Read raw data from MySQL
- Transform it into processed data
- Send data to Orion-LD

---

## Second Run (Optional / Faster)

### 6. Second run configuration
Set:
USE_PROCESSED_AS_SOURCE = True

### 7. Run semantic connector again
python semantic_connector.py

👉 This will:
- Skip transformation step
- Directly use processed data
- Send data to Orion-LD faster

---

## Run Dashboard

### 8. Start Streamlit
streamlit run app.py

## Access

| Service       | URL                   |
| ------------- | --------------------- |
| Orion-LD API  | http://localhost:1026 |
| Streamlit App | http://localhost:8501 |

---

## Verify Data

```bash
curl -H "Accept: application/ld+json" \
"http://localhost:1026/ngsi-ld/v1/entities"
```

---

## Current Scope

* Raw data ingestion (MySQL)
* Transformation to NGSI-LD
* Orion-LD integration
* Dashboard visualization

---

## Future Improvements

* Full SAREF ontology mapping
* Automated pipeline (remove manual flag)
* Advanced semantic enrichment
* Better error handling

---

## Important Notes

* MySQL runs locally (NOT Docker)
* Docker is only for MongoDB + Orion
* Run Python pipeline BEFORE dashboard
* Ensure DB credentials match `.env`

---

## Common Issues

### Empty dashboard

→ You forgot to set:

```python
USE_PROCESSED_AS_SOURCE = False
```

### MySQL connection error

→ Check credentials and server status

### Orion not responding

→ Ensure Docker is running

