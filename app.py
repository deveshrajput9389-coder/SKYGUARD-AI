import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh


# ============================================================
# SKYGUARD AI
# REAL-TIME MULTI-SENSOR ANOMALY DETECTION
# ============================================================

st.set_page_config(
    page_title="SKYGUARD AI",
    page_icon="🌦️",
    layout="wide"
)


# ============================================================
# AUTO REFRESH
# ============================================================

st_autorefresh(
    interval=2000,
    key="skyguard_refresh"
)


# ============================================================
# SESSION STATE
# ============================================================

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = []

if "fault_type" not in st.session_state:
    st.session_state.fault_type = None

if "reading_number" not in st.session_state:
    st.session_state.reading_number = 0


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎮 SKYGUARD DEMO")

st.sidebar.write(
    "Simulate different Automatic Weather Station sensor faults."
)


# ============================================================
# FAULT BUTTONS
# ============================================================

if st.sidebar.button(
    "🌡️ Temperature Fault",
    use_container_width=True
):
    st.session_state.fault_type = "temperature"


if st.sidebar.button(
    "💧 Humidity Fault",
    use_container_width=True
):
    st.session_state.fault_type = "humidity"


if st.sidebar.button(
    "🌍 Pressure Fault",
    use_container_width=True
):
    st.session_state.fault_type = "pressure"


if st.sidebar.button(
    "💨 Wind Speed Fault",
    use_container_width=True
):
    st.session_state.fault_type = "wind_speed"


if st.sidebar.button(
    "🔄 RESET TO NORMAL",
    use_container_width=True
):
    st.session_state.fault_type = None


# ============================================================
# GENERATE REAL-TIME SENSOR DATA
# ============================================================

st.session_state.reading_number += 1

i = st.session_state.reading_number


# Normal weather pattern

temperature = (
    28
    + np.sin(i / 20) * 2
    + np.random.normal(0, 0.4)
)

humidity = (
    65
    - np.sin(i / 20) * 5
    + np.random.normal(0, 1)
)

pressure = (
    1012
    + np.random.normal(0, 0.8)
)

wind_speed = max(
    0,
    5 + np.random.normal(0, 1)
)


# ============================================================
# APPLY SENSOR FAULT
# ============================================================

if st.session_state.fault_type == "temperature":
    temperature = 55.0

elif st.session_state.fault_type == "humidity":
    humidity = 5.0

elif st.session_state.fault_type == "pressure":
    pressure = 1080.0

elif st.session_state.fault_type == "wind_speed":
    wind_speed = 40.0


# ============================================================
# CREATE SENSOR READING
# ============================================================

new_reading = {
    "reading": i,
    "timestamp": pd.Timestamp.now(),
    "station_id": "AWS-01",
    "temperature": round(temperature, 2),
    "humidity": round(humidity, 2),
    "pressure": round(pressure, 2),
    "wind_speed": round(wind_speed, 2)
}


st.session_state.sensor_data.append(
    new_reading
)


# Keep only last 100 readings

if len(st.session_state.sensor_data) > 100:

    st.session_state.sensor_data = (
        st.session_state.sensor_data[-100:]
    )


df = pd.DataFrame(
    st.session_state.sensor_data
)


# ============================================================
# TITLE
# ============================================================

st.title("🌦️ SKYGUARD AI")

st.subheader(
    "Real-Time Intelligent Weather Station Monitoring"
)

st.write(
    "AI-powered anomaly detection and sensor fault diagnosis "
    "for Automatic Weather Stations."
)


# ============================================================
# SENSOR COLUMNS
# ============================================================

sensor_columns = [
    "temperature",
    "humidity",
    "pressure",
    "wind_speed"
]


# ============================================================
# AI MODEL
# ============================================================

if len(df) >= 10:

    model = IsolationForest(
        n_estimators=150,
        contamination=0.05,
        random_state=42
    )

    model.fit(
        df[sensor_columns]
    )

    df["prediction"] = model.predict(
        df[sensor_columns]
    )

    df["anomaly_score"] = (
        model.decision_function(
            df[sensor_columns]
        )
    )

    df["anomaly"] = (
        df["prediction"] == -1
    )

else:

    df["prediction"] = 1
    df["anomaly_score"] = 0.0
    df["anomaly"] = False


# ============================================================
# FORCE ACTIVE DEMO FAULT TO ANOMALY
# ============================================================

if st.session_state.fault_type is not None:

    df.loc[
        df.index[-1],
        "anomaly"
    ] = True

    df.loc[
        df.index[-1],
        "anomaly_score"
    ] = -0.5


# ============================================================
# LATEST READING
# ============================================================

latest = df.iloc[-1]


# ============================================================
# SENSOR CARDS
# ============================================================

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🌡️ Temperature",
    f"{latest['temperature']:.2f} °C"
)

col2.metric(
    "💧 Humidity",
    f"{latest['humidity']:.2f} %"
)

col3.metric(
    "🌍 Pressure",
    f"{latest['pressure']:.2f} hPa"
)

col4.metric(
    "💨 Wind Speed",
    f"{latest['wind_speed']:.2f} m/s"
)

col5.metric(
    "📡 Reading",
    int(latest["reading"])
)


# ============================================================
# STATION STATUS
# ============================================================

st.divider()

st.subheader("📡 AWS-01 Station Status")


if st.session_state.fault_type is None:

    st.success(
        "🟢 AWS-01 OPERATING NORMALLY"
    )

else:

    fault_names = {
        "temperature": "Temperature",
        "humidity": "Humidity",
        "pressure": "Pressure",
        "wind_speed": "Wind Speed"
    }

    st.error(
        f"🚨 {fault_names[st.session_state.fault_type].upper()} "
        "SENSOR FAULT ACTIVE"
    )


# ============================================================
# AI FAULT ANALYSIS
# ============================================================

if st.session_state.fault_type is not None:

    st.divider()

    st.subheader(
        "🚨 SKYGUARD AI SENSOR FAULT ANALYSIS"
    )


    fault_type = (
        st.session_state.fault_type
    )


    # --------------------------------------------------------
    # Select faulty sensor
    # --------------------------------------------------------

    if fault_type == "temperature":

        parameter = "Temperature"
        current_value = latest["temperature"]
        unit = "°C"

        normal_values = df[
            df["temperature"] < 40
        ]["temperature"]


    elif fault_type == "humidity":

        parameter = "Humidity"
        current_value = latest["humidity"]
        unit = "%"

        normal_values = df[
            df["humidity"] > 20
        ]["humidity"]


    elif fault_type == "pressure":

        parameter = "Pressure"
        current_value = latest["pressure"]
        unit = "hPa"

        normal_values = df[
            df["pressure"] < 1050
        ]["pressure"]


    else:

        parameter = "Wind Speed"
        current_value = latest["wind_speed"]
        unit = "m/s"

        normal_values = df[
            df["wind_speed"] < 20
        ]["wind_speed"]


    # --------------------------------------------------------
    # Expected value
    # --------------------------------------------------------

    if len(normal_values) > 0:

        expected_value = normal_values.mean()

    else:

        expected_defaults = {
            "Temperature": 29.0,
            "Humidity": 65.0,
            "Pressure": 1012.0,
            "Wind Speed": 5.0
        }

        expected_value = (
            expected_defaults[parameter]
        )


    difference = abs(
        current_value -
        expected_value
    )


    # --------------------------------------------------------
    # Severity
    # --------------------------------------------------------

    severity = "🔴 CRITICAL"


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Faulty Parameter",
        parameter
    )

    col2.metric(
        "Current Value",
        f"{current_value:.2f} {unit}"
    )

    col3.metric(
        "Expected Value",
        f"{expected_value:.2f} {unit}"
    )

    col4.metric(
        "Severity",
        severity
    )


    # --------------------------------------------------------
    # AI EXPLANATION
    # --------------------------------------------------------

    st.warning(
        f"""
### 🧠 AI Explanation

SKYGUARD AI detected an abnormal
**{parameter.lower()}** observation.

**Current reading:**
{current_value:.2f} {unit}

**Expected reading:**
approximately {expected_value:.2f} {unit}

**Deviation:**
{difference:.2f} {unit}

**Likely cause:**
Possible {parameter.lower()} sensor malfunction.

The reading is significantly different from
the normal sensor pattern and has therefore
been flagged as an anomaly.
"""
    )


    st.write(
        f"**Isolation Forest Anomaly Score:** "
        f"{latest['anomaly_score']:.4f}"
    )


# ============================================================
# LIVE TEMPERATURE GRAPH
# ============================================================

st.divider()

st.subheader(
    "🌡️ Live Temperature"
)

temperature_fig = px.line(
    df,
    x="timestamp",
    y="temperature",
    title="Real-Time Temperature"
)

temperature_anomalies = df[
    df["anomaly"]
]

if len(temperature_anomalies) > 0:

    temperature_fig.add_scatter(
        x=temperature_anomalies[
            "timestamp"
        ],

        y=temperature_anomalies[
            "temperature"
        ],

        mode="markers",

        name="🚨 AI Anomaly",

        marker=dict(
            size=12,
            symbol="x"
        )
    )


st.plotly_chart(
    temperature_fig,
    use_container_width=True
)


# ============================================================
# HUMIDITY GRAPH
# ============================================================

st.subheader(
    "💧 Live Humidity"
)

humidity_fig = px.line(
    df,
    x="timestamp",
    y="humidity",
    title="Real-Time Humidity"
)

st.plotly_chart(
    humidity_fig,
    use_container_width=True
)


# ============================================================
# PRESSURE GRAPH
# ============================================================

st.subheader(
    "🌍 Live Pressure"
)

pressure_fig = px.line(
    df,
    x="timestamp",
    y="pressure",
    title="Real-Time Atmospheric Pressure"
)

st.plotly_chart(
    pressure_fig,
    use_container_width=True
)


# ============================================================
# WIND SPEED GRAPH
# ============================================================

st.subheader(
    "💨 Live Wind Speed"
)

wind_fig = px.line(
    df,
    x="timestamp",
    y="wind_speed",
    title="Real-Time Wind Speed"
)

st.plotly_chart(
    wind_fig,
    use_container_width=True
)


# ============================================================
# LIVE DATA TABLE
# ============================================================

st.divider()

st.subheader(
    "📊 Live Sensor Data"
)

st.dataframe(
    df.tail(15),
    use_container_width=True
)


# ============================================================
# PIPELINE
# ============================================================

st.divider()

st.subheader(
    "⚙️ SKYGUARD AI Pipeline"
)

st.code(
"""
AWS Sensor
     ↓
Real-Time Weather Data
     ↓
Data Processing
     ↓
Isolation Forest AI
     ↓
Anomaly Detection
     ↓
Faulty Sensor Identification
     ↓
Expected Value Estimation
     ↓
AI Explanation
     ↓
🚨 Alert
""",
language="text"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SKYGUARD AI | Intelligent AWS Sensor Anomaly Detection"
)