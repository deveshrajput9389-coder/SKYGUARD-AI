import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh


# ============================================================
# SKYGUARD AI
# Intelligent Automatic Weather Station Monitoring
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SKYGUARD AI",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# AUTO REFRESH
# ============================================================

st_autorefresh(
    interval=2000,
    key="skyguard_auto_refresh"
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

if "event_log" not in st.session_state:
    st.session_state.event_log = []

if "previous_fault" not in st.session_state:
    st.session_state.previous_fault = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_event(message, event_type="INFO"):

    timestamp = pd.Timestamp.now().strftime("%H:%M:%S")

    st.session_state.event_log.append({
        "time": timestamp,
        "type": event_type,
        "event": message
    })

    # Keep last 30 events
    if len(st.session_state.event_log) > 30:
        st.session_state.event_log = (
            st.session_state.event_log[-30:]
        )


def get_expected_value(df, parameter):

    defaults = {
        "temperature": 29.0,
        "humidity": 65.0,
        "pressure": 1012.0,
        "wind_speed": 5.0
    }

    if parameter == "temperature":
        values = df[df["temperature"] < 40]["temperature"]

    elif parameter == "humidity":
        values = df[
            (df["humidity"] > 20) &
            (df["humidity"] < 90)
        ]["humidity"]

    elif parameter == "pressure":
        values = df[df["pressure"] < 1050]["pressure"]

    else:
        values = df[df["wind_speed"] < 20]["wind_speed"]

    if len(values) > 0:
        return values.mean()

    return defaults[parameter]


def calculate_health(df):

    if len(df) == 0:
        return 100

    latest = df.iloc[-1]

    score = 100

    # Temperature
    if latest["temperature"] > 40 or latest["temperature"] < -20:
        score -= 25

    # Humidity
    if latest["humidity"] < 20 or latest["humidity"] > 90:
        score -= 25

    # Pressure
    if latest["pressure"] > 1050 or latest["pressure"] < 950:
        score -= 25

    # Wind
    if latest["wind_speed"] > 20:
        score -= 25

    return max(0, score)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎮 SKYGUARD DEMO")

st.sidebar.caption(
    "Automatic Weather Station fault simulation"
)

st.sidebar.divider()

st.sidebar.subheader("🚨 Fault Injection")


if st.sidebar.button(
    "🌡️ Temperature Fault",
    use_container_width=True
):

    st.session_state.fault_type = "temperature"

    if st.session_state.previous_fault != "temperature":
        add_event(
            "Temperature sensor fault injected",
            "ALERT"
        )

    st.session_state.previous_fault = "temperature"


if st.sidebar.button(
    "💧 Humidity Fault",
    use_container_width=True
):

    st.session_state.fault_type = "humidity"

    if st.session_state.previous_fault != "humidity":
        add_event(
            "Humidity sensor fault injected",
            "ALERT"
        )

    st.session_state.previous_fault = "humidity"


if st.sidebar.button(
    "🌍 Pressure Fault",
    use_container_width=True
):

    st.session_state.fault_type = "pressure"

    if st.session_state.previous_fault != "pressure":
        add_event(
            "Pressure sensor fault injected",
            "ALERT"
        )

    st.session_state.previous_fault = "pressure"


if st.sidebar.button(
    "💨 Wind Speed Fault",
    use_container_width=True
):

    st.session_state.fault_type = "wind_speed"

    if st.session_state.previous_fault != "wind_speed":
        add_event(
            "Wind speed sensor fault injected",
            "ALERT"
        )

    st.session_state.previous_fault = "wind_speed"


if st.sidebar.button(
    "🔄 RESET TO NORMAL",
    use_container_width=True
):

    st.session_state.fault_type = None

    if st.session_state.previous_fault is not None:
        add_event(
            "All sensors returned to normal",
            "NORMAL"
        )

    st.session_state.previous_fault = None


st.sidebar.divider()

st.sidebar.info(
    "💡 Demo tip: Start with normal readings, "
    "then inject a fault and show the AI explanation."
)


# ============================================================
# GENERATE REAL-TIME SENSOR DATA
# ============================================================

st.session_state.reading_number += 1

reading_number = st.session_state.reading_number


# Normal weather behaviour

temperature = (
    28
    + np.sin(reading_number / 20) * 2
    + np.random.normal(0, 0.4)
)

humidity = (
    65
    - np.sin(reading_number / 20) * 5
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
# APPLY FAULT
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
    "reading": reading_number,
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


# Keep last 100 observations

if len(st.session_state.sensor_data) > 100:

    st.session_state.sensor_data = (
        st.session_state.sensor_data[-100:]
    )


df = pd.DataFrame(
    st.session_state.sensor_data
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🌦️ SKYGUARD AI")

st.markdown(
    "**Intelligent Automatic Weather Station Monitoring & "
    "Sensor Anomaly Detection**"
)


header_col1, header_col2, header_col3 = st.columns(3)


with header_col1:

    st.markdown(
        "**📡 Station:** `AWS-01`"
    )


with header_col2:

    st.markdown(
        "**🌐 Connection:** 🟢 ONLINE"
    )


with header_col3:

    current_time = pd.Timestamp.now().strftime(
        "%H:%M:%S"
    )

    st.markdown(
        f"**🕐 Last Update:** `{current_time}`"
    )


# ============================================================
# AI MODEL — CLEAN BASELINE
# ============================================================

sensor_columns = [
    "temperature",
    "humidity",
    "pressure",
    "wind_speed"
]


# ------------------------------------------------------------
# Create a clean NORMAL reference dataset
# ------------------------------------------------------------

np.random.seed(42)

baseline_size = 300

baseline = pd.DataFrame({

    "temperature":
        29
        + np.random.normal(0, 1.2, baseline_size),

    "humidity":
        65
        + np.random.normal(0, 4, baseline_size),

    "pressure":
        1012
        + np.random.normal(0, 2, baseline_size),

    "wind_speed":
        5
        + np.random.normal(0, 1.2, baseline_size)
})


# Keep values physically reasonable

baseline["humidity"] = baseline["humidity"].clip(30, 85)

baseline["pressure"] = baseline["pressure"].clip(
    995,
    1030
)

baseline["wind_speed"] = baseline["wind_speed"].clip(
    0,
    15
)


# ------------------------------------------------------------
# Train AI only on NORMAL data
# ------------------------------------------------------------

model = IsolationForest(
    n_estimators=200,
    contamination="auto",
    random_state=42
)

model.fit(
    baseline[sensor_columns]
)


# ------------------------------------------------------------
# Analyze current readings
# ------------------------------------------------------------

df["prediction"] = model.predict(
    df[sensor_columns]
)

df["anomaly_score"] = model.decision_function(
    df[sensor_columns]
)

df["anomaly"] = (
    df["prediction"] == -1
)


# ============================================================
# PHYSICAL / ENGINEERING LIMIT CHECK
# ============================================================

latest_index = df.index[-1]

latest_temperature = df.loc[
    latest_index,
    "temperature"
]

latest_humidity = df.loc[
    latest_index,
    "humidity"
]

latest_pressure = df.loc[
    latest_index,
    "pressure"
]

latest_wind = df.loc[
    latest_index,
    "wind_speed"
]


engineering_fault = False


# Temperature
if (
    latest_temperature > 45
    or latest_temperature < -10
):
    engineering_fault = True


# Humidity
if (
    latest_humidity < 10
    or latest_humidity > 95
):
    engineering_fault = True


# Pressure
if (
    latest_pressure > 1060
    or latest_pressure < 940
):
    engineering_fault = True


# Wind speed
if latest_wind > 30:
    engineering_fault = True


# ============================================================
# FINAL AI DECISION
# ============================================================

if engineering_fault:

    df.loc[
        latest_index,
        "anomaly"
    ] = True

elif st.session_state.fault_type is not None:

    # Deterministic demo fault
    df.loc[
        latest_index,
        "anomaly"
    ] = True

else:

    # Normal operation
    df.loc[
        latest_index,
        "anomaly"
    ] = False
# ============================================================
# LATEST READING
# ============================================================

latest = df.iloc[-1]


# ============================================================
# SYSTEM HEALTH
# ============================================================

system_health = calculate_health(df)


# ============================================================
# TOP STATUS BAR
# ============================================================

st.divider()

status_col1, status_col2, status_col3, status_col4 = st.columns(4)


with status_col1:

    st.metric(
        "📊 System Health",
        f"{system_health}%"
    )


with status_col2:

    st.metric(
        "📡 Total Readings",
        int(len(df))
    )


with status_col3:

    anomaly_count = int(
        df["anomaly"].sum()
    )

    st.metric(
        "🚨 Anomalies",
        anomaly_count
    )


with status_col4:

    st.metric(
        "🤖 AI Engine",
        "ACTIVE"
    )


# ============================================================
# SENSOR READINGS
# ============================================================

st.subheader("📡 Live AWS Sensor Readings")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌡️ Temperature",
        f"{latest['temperature']:.2f} °C"
    )


with col2:

    st.metric(
        "💧 Humidity",
        f"{latest['humidity']:.2f} %"
    )


with col3:

    st.metric(
        "🌍 Pressure",
        f"{latest['pressure']:.2f} hPa"
    )


with col4:

    st.metric(
        "💨 Wind Speed",
        f"{latest['wind_speed']:.2f} m/s"
    )


# ============================================================
# SENSOR HEALTH
# ============================================================

st.divider()

st.subheader("🩺 Sensor Health")


def sensor_status(parameter):

    if st.session_state.fault_type == parameter:
        return "🔴 FAULT"

    return "🟢 NORMAL"


health_col1, health_col2, health_col3, health_col4 = st.columns(4)


with health_col1:

    st.info(
        f"🌡️ **Temperature**\n\n"
        f"{sensor_status('temperature')}"
    )


with health_col2:

    st.info(
        f"💧 **Humidity**\n\n"
        f"{sensor_status('humidity')}"
    )


with health_col3:

    st.info(
        f"🌍 **Pressure**\n\n"
        f"{sensor_status('pressure')}"
    )


with health_col4:

    st.info(
        f"💨 **Wind Speed**\n\n"
        f"{sensor_status('wind_speed')}"
    )


# ============================================================
# STATION STATUS
# ============================================================

st.divider()

if st.session_state.fault_type is None:

    st.success(
        "🟢 AWS-01 OPERATING NORMALLY — "
        "No active simulated sensor fault."
    )

else:

    fault_names = {
        "temperature": "TEMPERATURE",
        "humidity": "HUMIDITY",
        "pressure": "PRESSURE",
        "wind_speed": "WIND SPEED"
    }

    st.error(
        f"🚨 {fault_names[st.session_state.fault_type]} "
        "SENSOR FAULT ACTIVE"
    )


# ============================================================
# AI ANALYSIS
# ============================================================

if st.session_state.fault_type is not None:

    st.divider()

    st.subheader(
        "🚨 SKYGUARD AI FAULT ANALYSIS"
    )


    fault_type = st.session_state.fault_type


    if fault_type == "temperature":

        parameter = "Temperature"
        current_value = latest["temperature"]
        unit = "°C"


    elif fault_type == "humidity":

        parameter = "Humidity"
        current_value = latest["humidity"]
        unit = "%"


    elif fault_type == "pressure":

        parameter = "Pressure"
        current_value = latest["pressure"]
        unit = "hPa"


    else:

        parameter = "Wind Speed"
        current_value = latest["wind_speed"]
        unit = "m/s"


    expected_value = get_expected_value(
        df,
        fault_type
    )


    deviation = abs(
        current_value -
        expected_value
    )


    # --------------------------------------------------------
    # Derived risk indicator
    # --------------------------------------------------------

    risk_confidence = min(
        99,
        max(
            85,
            int(
                85 +
                min(
                    deviation,
                    14
                )
            )
        )
    )


    analysis_col1, analysis_col2, analysis_col3, analysis_col4 = (
        st.columns(4)
    )


    with analysis_col1:

        st.metric(
            "Faulty Parameter",
            parameter
        )


    with analysis_col2:

        st.metric(
            "Current Value",
            f"{current_value:.2f} {unit}"
        )


    with analysis_col3:

        st.metric(
            "Expected Value",
            f"{expected_value:.2f} {unit}"
        )


    with analysis_col4:

        st.metric(
            "Severity",
            "🔴 CRITICAL"
        )


    # --------------------------------------------------------
    # AI confidence
    # --------------------------------------------------------

    st.markdown(
        f"### 🤖 AI Detection Confidence — {risk_confidence}%"
    )

    st.progress(
        risk_confidence / 100
    )

    st.caption(
        "This is a demo risk/confidence indicator derived "
        "from the magnitude of the detected deviation; "
        "it is not a calibrated probability."
    )


    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    st.warning(
        f"""
### 🧠 Why SKYGUARD flagged this reading

**Parameter:** {parameter}

**Current reading:** {current_value:.2f} {unit}

**Expected reading:** approximately {expected_value:.2f} {unit}

**Deviation:** {deviation:.2f} {unit}

**Possible cause:** {parameter} sensor malfunction.

The observation is significantly different from the
recent normal sensor behaviour and has been flagged
for investigation.
"""
    )


    st.write(
        f"**Isolation Forest Anomaly Score:** "
        f"`{latest['anomaly_score']:.4f}`"
    )


# ============================================================
# LIVE TEMPERATURE GRAPH
# ============================================================

st.divider()

st.subheader("🌡️ Temperature Monitoring")


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
        x=temperature_anomalies["timestamp"],
        y=temperature_anomalies["temperature"],
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
# OTHER SENSOR GRAPHS
# ============================================================

graph_col1, graph_col2 = st.columns(2)


with graph_col1:

    humidity_fig = px.line(
        df,
        x="timestamp",
        y="humidity",
        title="💧 Humidity"
    )

    st.plotly_chart(
        humidity_fig,
        use_container_width=True
    )


with graph_col2:

    pressure_fig = px.line(
        df,
        x="timestamp",
        y="pressure",
        title="🌍 Atmospheric Pressure"
    )

    st.plotly_chart(
        pressure_fig,
        use_container_width=True
    )


wind_fig = px.line(
    df,
    x="timestamp",
    y="wind_speed",
    title="💨 Wind Speed"
)


st.plotly_chart(
    wind_fig,
    use_container_width=True
)


# ============================================================
# EVENT LOG
# ============================================================

st.divider()

st.subheader("📋 Event Log")


if len(st.session_state.event_log) > 0:

    event_df = pd.DataFrame(
        st.session_state.event_log[::-1]
    )

    st.dataframe(
        event_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No events yet. SKYGUARD is monitoring AWS-01."
    )


# ============================================================
# ANOMALY HISTORY
# ============================================================

st.divider()

st.subheader("🚨 Anomaly History")


anomaly_history = df[
    df["anomaly"]
][
    [
        "reading",
        "timestamp",
        "station_id",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "anomaly_score"
    ]
]


if len(anomaly_history) > 0:

    st.dataframe(
        anomaly_history.tail(20),
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "🟢 No anomalies detected."
    )


# ============================================================
# LIVE DATA
# ============================================================

st.divider()

with st.expander(
    "📊 View Raw Live Sensor Data"
):

    st.dataframe(
        df.tail(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SYSTEM ARCHITECTURE
# ============================================================

st.divider()

st.subheader(
    "⚙️ SKYGUARD AI Architecture"
)


st.code(
"""
Automatic Weather Station
          │
          ▼
   Sensor Observations
          │
          ▼
    Data Processing
          │
          ▼
    Isolation Forest
          │
          ▼
   Anomaly Detection
          │
     ┌────┴────┐
     ▼         ▼
  NORMAL    ANOMALY
    🟢         🚨
                │
                ▼
        Fault Identification
                │
                ▼
        Expected Value
                │
                ▼
       AI Explanation
                │
                ▼
          Alert / Log
""",
language="text"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SKYGUARD AI • Intelligent Automatic Weather Station "
    "Anomaly Detection • SIH Prototype"
)
