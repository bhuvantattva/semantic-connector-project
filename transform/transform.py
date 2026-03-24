import json
from config.db_config import get_raw_db, get_processed_db

raw_conn = get_raw_db()
raw_cursor = raw_conn.cursor(dictionary=True)

processed_conn = get_processed_db()
processed_cursor = processed_conn.cursor()

raw_cursor.execute("SELECT * FROM raw_data")

for row in raw_cursor.fetchall():
    payload = json.loads(row["payload"])

    device_id = row["device_id"]
    device_type = row["device_type"]

    for key, value in payload.items():

        unit = None

        # Basic unit mapping (important for demo explanation)
        if key in ["temperature"]:
            unit = "C"
        elif key in ["humidity"]:
            unit = "%"
        elif key in ["power", "power_output", "charging_power"]:
            unit = "W"
        elif key in ["voltage"]:
            unit = "V"

        # Convert power to kW (optional normalization)
        if key in ["power", "power_output", "charging_power"] and value is not None:
            value = value / 1000
            unit = "kW"

        query = """
        INSERT INTO standardized_data 
        (device_id, device_type, attribute_name, attribute_value, unit)
        VALUES (%s, %s, %s, %s, %s)
        """

        processed_cursor.execute(query, (
            device_id,
            device_type,
            key,
            str(value),
            unit
        ))

processed_conn.commit()
print("Data Transformed Successfully")
