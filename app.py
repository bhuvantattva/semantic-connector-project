# ===============================
# 1. IMPORT LIBRARIES
# ===============================
import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh


# ===============================
# 2. AUTO REFRESH SETUP
# ===============================
st_autorefresh(interval=5000, key="refresh")


# ===============================
# 3. PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Smart Home Dashboard",
    layout="wide"
)

st.title("🏠 Smart Home Dashboard")


# ===============================
# 4. DEVICE TYPE SELECTION
# ===============================
device_type = st.selectbox(
    "Select Device Type",
    [
        "smart_meter",
        "thermostat",
        "camera",
        "ev_charger",
        "humidity_sensor",
        "solar_inverter",
        "smart_light",
        "door_lock"
    ]
)


# ===============================
# 5. ORION-LD API CONFIGURATION
# ===============================
url = f"http://localhost:1026/ngsi-ld/v1/entities?type={device_type}"

headers = {
    "Accept": "application/ld+json"
}


# ===============================
# 6. FETCH DATA FROM ORION
# ===============================
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"Error connecting to Orion-LD: {e}")
    st.stop()


# ===============================
# 7. HANDLE API ERRORS
# ===============================
if isinstance(data, dict):
    st.error(data)
    st.stop()


# ===============================
# 8. TRANSFORM NGSI-LD TO TABLE FORMAT
# ===============================
rows = []

for item in data:
    if not isinstance(item, dict):
        continue

    row = {
        "id": item.get("id"),
        "type": item.get("type")
    }

    for key, val in item.items():
        if isinstance(val, dict) and "value" in val:
            row[key] = val["value"]

    rows.append(row)

df = pd.DataFrame(rows)


# ===============================
# 9. CLEAN NUMERIC COLUMNS
# ===============================
def clean_numeric_column(series):
    """
    Convert mixed text/numeric values safely to numeric.
    Invalid values become NaN.
    """
    return pd.to_numeric(
        series.astype(str)
              .str.replace("°C", "", regex=False)
              .str.replace("%", "", regex=False)
              .str.replace("kW", "", regex=False)
              .str.replace("W", "", regex=False)
              .str.replace(",", "", regex=False)
              .str.strip(),
        errors="coerce"
    )

numeric_columns = [
    "temperature",
    "power",
    "humidity",
    "voltage",
    "charging_power",
    "power_output",
    "brightness",
    "battery"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = clean_numeric_column(df[col])


# ===============================
# 10. DISPLAY DATA TABLE
# ===============================
st.subheader("📊 Device Data")
st.dataframe(df, use_container_width=True)


# ===============================
# 11. VISUALIZATION (CHARTS)
# ===============================
st.subheader("📈 Insights")

col1, col2 = st.columns(2)

with col1:
    if "power" in df.columns:
        power_df = df["power"].dropna()
        if not power_df.empty:
            st.markdown("### ⚡ Power Consumption")
            st.bar_chart(power_df)
        else:
            st.info("No valid power data available.")

with col2:
    if "temperature" in df.columns:
        temp_df = df["temperature"].dropna()
        if not temp_df.empty:
            st.markdown("### 🌡️ Temperature")
            st.line_chart(temp_df)
        else:
            st.info("No valid temperature data available.")


# ===============================
# 12. KPI SUMMARY SECTION
# ===============================
st.subheader("📌 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Devices", len(df))

with col2:
    if "power" in df.columns:
        avg_power = df["power"].dropna().mean()
        st.metric("Avg Power", round(avg_power, 2) if pd.notna(avg_power) else "N/A")
    else:
        st.metric("Avg Power", "N/A")

with col3:
    if "temperature" in df.columns:
        avg_temp = df["temperature"].dropna().mean()
        st.metric("Avg Temp", round(avg_temp, 2) if pd.notna(avg_temp) else "N/A")
    else:
        st.metric("Avg Temp", "N/A")
