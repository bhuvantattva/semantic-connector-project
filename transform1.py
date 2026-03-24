import json
from config.db_config import get_raw_db, get_processed_db

raw_conn = get_raw_db()
raw_cursor = raw_conn.cursor(dictionary=True)

processed_conn = get_processed_db()
processed_cursor = processed_conn.cursor()

raw_cursor.execute("SELECT * FROM raw_data")

devices = {}

for row in raw_cursor.fetchall():
    payload = json.loads(row["payload"])

    device_id = row["device_id"]
    device_type = row["device_type"]

    if device_id not in devices:
        devices[device_id] = {
            "device_type": device_type,
            "temperature": None,
            "energy_consumption": None,
            "voltage": None,
            "unit": None,
            "motion_detected": None,
            "event_timestamp": None,
            "charging_power": None,
            "vehicle_connected": None
        }

    # Thermostat / environmental sensors
    if "temperature" in payload:
        devices[device_id]["temperature"] = payload["temperature"]

    if "unit" in payload:
        devices[device_id]["unit"] = payload["unit"]

    # Smart meter / inverter / charger power
    if "power" in payload and payload["power"] is not None:
        devices[device_id]["energy_consumption"] = payload["power"] / 1000

    if "power_output" in payload and payload["power_output"] is not None:
        devices[device_id]["energy_consumption"] = payload["power_output"] / 1000

    if "charging_power" in payload and payload["charging_power"] is not None:
        devices[device_id]["charging_power"] = payload["charging_power"] / 1000

    if "voltage" in payload:
        devices[device_id]["voltage"] = payload["voltage"]

    # Camera / event-based devices
    if "motion_detected" in payload:
        devices[device_id]["motion_detected"] = payload["motion_detected"]

    if "timestamp" in payload and payload["timestamp"]:
        devices[device_id]["event_timestamp"] = payload["timestamp"].replace("T", " ")

    # EV charger connection status
    if "vehicle_connected" in payload:
        devices[device_id]["vehicle_connected"] = payload["vehicle_connected"]

query = """
INSERT INTO standardized_data (
    device_id,
    device_type,
    temperature,
    energy_consumption,
    voltage,
    unit,
    motion_detected,
    event_timestamp,
    charging_power,
    vehicle_connected
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for device_id, values in devices.items():
    processed_cursor.execute(query, (
        device_id,
        values["device_type"],
        values["temperature"],
        values["energy_consumption"],
        values["voltage"],
        values["unit"],
        values["motion_detected"],
        values["event_timestamp"],
        values["charging_power"],
        values["vehicle_connected"]
    ))

processed_conn.commit()

raw_cursor.close()
processed_cursor.close()
raw_conn.close()
processed_conn.close()

print("Data Transformed Successfully")