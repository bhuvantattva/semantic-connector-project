# ===============================
# 1. IMPORT LIBRARIES
# ===============================
import mysql.connector
import pandas as pd
import json
import requests


# ===============================
# CONFIG (SWITCH PIPELINE MODE)
# ===============================
USE_PROCESSED_AS_SOURCE = True   # 🔥 True = use processed table → Orion


# ===============================
# 2. CONNECT TO MYSQL
# ===============================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="smart_home"
)

cursor = conn.cursor()


# ===============================
# 3. DELETE OLD DATA FROM ORION 🔥
# ===============================
def delete_orion_data():
    print("\n🔹 DELETING OLD ENTITIES")

    BASE_URL = "http://localhost:1026/ngsi-ld/v1/entities"
    HEADERS = {"Accept": "application/ld+json"}

    device_types = [
        "smart_meter", "thermostat", "camera", "ev_charger",
        "humidity_sensor", "solar_inverter", "smart_light", "door_lock"
    ]

    for dtype in device_types:
        get_url = f"{BASE_URL}?type={dtype}"
        response = requests.get(get_url, headers=HEADERS)

        if response.status_code == 200:
            entities = response.json()

            for entity in entities:
                entity_id = entity["id"]
                delete_url = f"{BASE_URL}/{entity_id}"

                del_res = requests.delete(delete_url)
                print(f"Deleted {entity_id}: {del_res.status_code}")


# ===============================
# 4. FETCH RAW DATA
# ===============================
def fetch_raw_data():
    query = "SELECT * FROM raw_device_data_table"
    df = pd.read_sql(query, conn)

    print("\n🔹 RAW DATA")
    print(df)

    return df


# ===============================
# 5. TRANSFORM TO NGSI-LD
# ===============================
def transform_to_ngsi_ld(row):
    payload = row['raw_payload']

    if isinstance(payload, str):
        payload = json.loads(payload)

    entity = {
        "id": f"urn:ngsi-ld:{row['device_type']}:{row['device_id']}",
        "type": row['device_type'],
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }

    for key, value in payload.items():
        entity[key] = {
            "type": "Property",
            "value": value
        }

    return entity


# ===============================
# 6. STORE INTO PROCESSED TABLE
# ===============================
def store_processed_data(entity):
    entity_id = entity["id"]
    entity_type = entity["type"]

    for key, val in entity.items():
        if isinstance(val, dict) and "value" in val:

            cursor.execute("""
                INSERT INTO processed_device_data 
                (entity_id, entity_type, attribute_name, attribute_value)
                VALUES (%s, %s, %s, %s)
            """, (
                entity_id,
                entity_type,
                key,
                str(val["value"])
            ))


# ===============================
# 7. FETCH FROM PROCESSED TABLE 🔥
# ===============================
def fetch_processed_data():
    query = """
    SELECT entity_id, entity_type, attribute_name, attribute_value
    FROM processed_device_data
    """
    df = pd.read_sql(query, conn)
    return df


# ===============================
# 8. REBUILD NGSI FROM PROCESSED
# ===============================
def rebuild_ngsi(df):
    entities = {}

    for _, row in df.iterrows():
        eid = row['entity_id']

        if eid not in entities:
            entities[eid] = {
                "id": eid,
                "type": row['entity_type'],
                "@context": [
                    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
                ]
            }

        entities[eid][row['attribute_name']] = {
            "type": "Property",
            "value": row['attribute_value']
        }

    return list(entities.values())


# ===============================
# 9. SEND TO ORION
# ===============================
def send_to_orion(entities):
    ORION_URL = "http://localhost:1026/ngsi-ld/v1/entities"
    HEADERS = {"Content-Type": "application/ld+json"}

    print("\n🔹 SENDING TO ORION")

    for entity in entities:
        response = requests.post(ORION_URL, json=entity, headers=HEADERS)
        print(response.status_code, response.text)


# ===============================
# 🔥 MAIN PIPELINE EXECUTION
# ===============================
delete_orion_data()

if not USE_PROCESSED_AS_SOURCE:
    # 🔵 RAW → NGSI → PROCESSED → ORION
    df = fetch_raw_data()
    ngsi_data = df.apply(transform_to_ngsi_ld, axis=1)

    print("\n🔹 STORING PROCESSED DATA")
    for entity in ngsi_data:
        store_processed_data(entity)

    conn.commit()

    print("\n🔹 NGSI-LD DATA")
    for item in ngsi_data:
        print(item)

    send_to_orion(ngsi_data)

else:
    # 🔴 PROCESSED → NGSI → ORION
    print("\n🔹 USING PROCESSED TABLE AS SOURCE")

    processed_df = fetch_processed_data()
    entities = rebuild_ngsi(processed_df)

    send_to_orion(entities)


# ===============================
# 10. CLOSE CONNECTION
# ===============================
cursor.close()
conn.close()
