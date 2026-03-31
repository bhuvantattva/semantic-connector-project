import requests

print("🔹 DELETING OLD ENTITIES")

BASE_URL = "http://localhost:1026/ngsi-ld/v1/entities"
HEADERS = {"Accept": "application/ld+json"}

# 🔥 All your device types
device_types = [
    "smart_meter",
    "thermostat",
    "camera",
    "ev_charger",
    "humidity_sensor",
    "solar_inverter",
    "smart_light",
    "door_lock"
]

for dtype in device_types:

    print(f"\n➡️ Processing type: {dtype}")

    # ✅ Fetch entities by type (required!)
    get_url = f"{BASE_URL}?type={dtype}"

    response = requests.get(get_url, headers=HEADERS)

    if response.status_code == 200:
        entities = response.json()

        for entity in entities:
            entity_id = entity["id"]

            delete_url = f"{BASE_URL}/{entity_id}"
            del_res = requests.delete(delete_url)

            print(f"Deleted {entity_id}: {del_res.status_code}")

    else:
        print(f"❌ Failed for {dtype}: {response.text}")
