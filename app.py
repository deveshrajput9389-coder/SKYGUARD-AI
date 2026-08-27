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
        "Time": timestamp,
        "Type": event_type,
        "Event": message
    })

    # Keep latest 30 events
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

        values = df[
            (df["temperature"] > -10) &
            (df["temperature"] < 45)
        ]["temperature"]

    elif parameter == "humidity":

        values = df[
            (df["humidity"] > 10) &
            (df["humidity"] < 95)
        ]["humidity"]

    elif parameter == "pressure":

        values = df[
            (df["pressure"] > 940) &
            (df["pressure"] < 1060)
        ]["pressure"]

    else:

        values = df[
            (df["wind_speed"] >= 0) &
            (df["wind_speed"] < 30)
        ]["wind_speed"]

    if len(values) > 0:
        return values.mean()

    return defaults[parameter]


def calculate_system_health(fault_type):

    if fault_type is None:
        return 100

    return 75


def get_sensor_status(parameter, fault_type):

    if fault_type == parameter:
        return "🔴 FAULT"

    return "🟢 NORMAL"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎮 SKYGUARD DEMO")

st.sidebar.caption(
    "Automatic Weather Station fault simulation"
)

st.sidebar.divider()

st.sidebar.subheader("🚨 Fault Injection")


# ------------------------------------------------------------
# Temperature fault
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Humidity fault
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Pressure fault
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Wind fault
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Reset
# ------------------------------------------------------------

if st.sidebar.button(
    "🔄 RESET TO NORMAL",
    use_container_width=True
):

    if st.session_state.fault_type is not None:

        add_event(
            "All sensors returned to normal",
            "NORMAL"
        )

    st.session_state.fault_type = None
    st.session_state.previous_fault = None


st.sidebar.divider()

st.sidebar.info(
    """
💡 **Demo sequence**

1. Start with normal readings
2. Show 🟢 NORMAL
3. Click a fault button
4. Show 🚨 AI detection
5. Explain expected value
6. Press RESET TO NORMAL
"""
)


# ============================================================
# GENERATE NORMAL SENSOR DATA
# ============================================================

st.session_state.reading_number += 1

reading_number = st.session_state.reading_number


# Create realistic smooth weather behaviour

temperature = (
    29
    + np.sin(reading_number / 15) * 1.5
    + np.random.normal(0, 0.25)
)


humidity = (
    65
    - np.sin(reading_number / 15) * 4
    + np.random.normal(0, 0.7)
)


pressure = (
    1012
    + np.sin(reading_number / 30) * 2
    + np.random.normal(0, 0.5)
)


wind_speed = max(
    0,
    5
    + np.sin(reading_number / 10)
    + np.random.normal(0, 0.5)
)


# ============================================================
# APPLY SIMULATED SENSOR FAULT
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
# CREATE CURRENT READING
# ============================================================

new_reading = {

    "reading": reading_number,

    "timestamp": pd.Timestamp.now(),

    "station_id": "AWS-01",

    "temperature": round(
        temperature,
        2
    ),

    "humidity": round(
        humidity,
        2
    ),

    "pressure": round(
        pressure,
        2
    ),

    "wind_speed": round(
        wind_speed,
        2
    )
}


st.session_state.sensor_data.append(
    new_reading
)


# Keep latest 100 readings

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
    """
**Intelligent Automatic Weather Station Monitoring & Sensor Anomaly Detection**
"""
)


header1, header2, header3 = st.columns(3)


with header1:

    st.markdown(
        "**📡 Station:** `AWS-01`"
    )


with header2:

    st.markdown(
        "**🌐 Connection:** 🟢 ONLINE"
    )


with header3:

    current_time = pd.Timestamp.now().strftime(
        "%H:%M:%S"
    )

    st.markdown(
        f"**🕐 Last Update:** `{current_time}`"
    )


# ============================================================
# AI MODEL
# CLEAN NORMAL BASELINE
# ============================================================

sensor_columns = [
    "temperature",
    "humidity",
    "pressure",
    "wind_speed"
]


# ------------------------------------------------------------
# Generate clean NORMAL training data
# ------------------------------------------------------------

np.random.seed(42)

baseline_size = 500


baseline = pd.DataFrame({

    "temperature":
        29
        + np.random.normal(
            0,
            1.2,
            baseline_size
        ),

    "humidity":
        65
        + np.random.normal(
            0,
            4,
            baseline_size
        ),

    "pressure":
        1012
        + np.random.normal(
            0,
            2,
            baseline_size
        ),

    "wind_speed":
        5
        + np.random.normal(
            0,
            1.2,
            baseline_size
        )
})


# Keep baseline physically reasonable

baseline["temperature"] = baseline[
    "temperature"
].clip(
    -5,
    45
)


baseline["humidity"] = baseline[
    "humidity"
].clip(
    30,
    85
)


baseline["pressure"] = baseline[
    "pressure"
].clip(
    995,
    1030
)


baseline["wind_speed"] = baseline[
    "wind_speed"
].clip(
    0,
    15
)


# ------------------------------------------------------------
# Train Isolation Forest
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
# AI prediction
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
# ENGINEERING SANITY CHECK
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


# Temperature limits

if (
    latest_temperature > 45
    or latest_temperature < -10
):

    engineering_fault = True


# Humidity limits

if (
    latest_humidity < 10
    or latest_humidity > 95
):

    engineering_fault = True


# Pressure limits

if (
    latest_pressure > 1060
    or latest_pressure < 940
):

    engineering_fault = True


# Wind limits

if latest_wind > 30:

    engineering_fault = True


# ============================================================
# FINAL DECISION
# ============================================================

# For this prototype we deliberately make the
# fault-injection controls deterministic.

if st.session_state.fault_type is not None:

    df.loc[
        latest_index,
        "anomaly"
    ] = True


elif engineering_fault:

    df.loc[
        latest_index,
        "anomaly"
    ] = True


else:

    # Normal operating condition
    # is considered normal.

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

system_health = calculate_system_health(
    st.session_state.fault_type
)


# ============================================================
# TOP STATUS BAR
# ============================================================

st.divider()


status1, status2, status3, status4 = st.columns(4)


with status1:

    st.metric(
        "📊 System Health",
        f"{system_health}%"
    )


with status2:

    st.metric(
        "📡 Total Readings",
        int(len(df))
    )


with status3:

    # CURRENT anomaly, not historical count

    current_anomaly = int(
        bool(
            latest["anomaly"]
        )
    )

    st.metric(
        "🚨 Current Anomaly",
        current_anomaly
    )


with status4:

    st.metric(
        "🤖 AI Engine",
        "ACTIVE"
    )


# ============================================================
# LIVE SENSOR READINGS
# ============================================================

st.subheader(
    "📡 Live AWS Sensor Readings"
)


sensor1, sensor2, sensor3, sensor4 = st.columns(4)


with sensor1:

    st.metric(
        "🌡️ Temperature",
        f"{latest['temperature']:.2f} °C"
    )


with sensor2:

    st.metric(
        "💧 Humidity",
        f"{latest['humidity']:.2f} %"
    )


with sensor3:

    st.metric(
        "🌍 Pressure",
        f"{latest['pressure']:.2f} hPa"
    )


with sensor4:

    st.metric(
        "💨 Wind Speed",
        f"{latest['wind_speed']:.2f} m/s"
    )


# ============================================================
# SENSOR HEALTH
# ============================================================

st.divider()

st.subheader(
    "🩺 Sensor Health"
)


health1, health2, health3, health4 = st.columns(4)


with health1:

    status = get_sensor_status(
        "temperature",
        st.session_state.fault_type
    )

    st.info(
        f"""
🌡️ **Temperature**

{status}
"""
    )


with health2:

    status = get_sensor_status(
        "humidity",
        st.session_state.fault_type
    )

    st.info(
        f"""
💧 **Humidity**

{status}
"""
    )


with health3:

    status = get_sensor_status(
        "pressure",
        st.session_state.fault_type
    )

    st.info(
        f"""
🌍 **Pressure**

{status}
"""
    )


with health4:

    status = get_sensor_status(
        "wind_speed",
        st.session_state.fault_type
    )

    st.info(
        f"""
💨 **Wind Speed**

{status}
"""
    )


# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider()


if st.session_state.fault_type is None:

    st.success(
        """
🟢 **AWS-01 OPERATING NORMALLY**

All monitored parameters are within expected operating behaviour.
"""
    )

else:

    fault_names = {

        "temperature":
            "TEMPERATURE",

        "humidity":
            "HUMIDITY",

        "pressure":
            "PRESSURE",

        "wind_speed":
            "WIND SPEED"
    }


    st.error(
        f"""
🚨 **{fault_names[st.session_state.fault_type]}
SENSOR FAULT ACTIVE**
"""
    )


# ============================================================
# AI ANALYSIS
# ============================================================

if st.session_state.fault_type is not None:

    st.divider()

    st.subheader(
        "🚨 SKYGUARD AI FAULT ANALYSIS"
    )


    fault_type = (
        st.session_state.fault_type
    )


    # --------------------------------------------------------
    # Determine parameter
    # --------------------------------------------------------

    if fault_type == "temperature":

        parameter = "Temperature"

        current_value = latest[
            "temperature"
        ]

        unit = "°C"


    elif fault_type == "humidity":

        parameter = "Humidity"

        current_value = latest[
            "humidity"
        ]

        unit = "%"


    elif fault_type == "pressure":

        parameter = "Pressure"

        current_value = latest[
            "pressure"
        ]

        unit = "hPa"


    else:

        parameter = "Wind Speed"

        current_value = latest[
            "wind_speed"
        ]

        unit = "m/s"


    # --------------------------------------------------------
    # Expected value
    # --------------------------------------------------------

    expected_value = get_expected_value(
        df,
        fault_type
    )


    # For fault mode, calculate expected value
    # from the clean baseline instead of faulty value.

    if fault_type == "temperature":

        expected_value = baseline[
            "temperature"
        ].mean()


    elif fault_type == "humidity":

        expected_value = baseline[
            "humidity"
        ].mean()


    elif fault_type == "pressure":

        expected_value = baseline[
            "pressure"
        ].mean()


    elif fault_type == "wind_speed":

        expected_value = baseline[
            "wind_speed"
        ].mean()


    deviation = abs(
        current_value -
        expected_value
    )


    # --------------------------------------------------------
    # Derived confidence indicator
    # --------------------------------------------------------

    confidence = min(
        99,
        max(
            90,
            int(
                90
                + min(
                    deviation,
                    9
                )
            )
        )
    )


    analysis1, analysis2, analysis3, analysis4 = (
        st.columns(4)
    )


    with analysis1:

        st.metric(
            "Faulty Parameter",
            parameter
        )


    with analysis2:

        st.metric(
            "Current Value",
            f"{current_value:.2f} {unit}"
        )


    with analysis3:

        st.metric(
            "Expected Value",
            f"{expected_value:.2f} {unit}"
        )


    with analysis4:

        st.metric(
            "Severity",
            "🔴 CRITICAL"
        )


    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    st.markdown(
        f"""
### 🤖 AI Detection Confidence — {confidence}%
"""
    )


    st.progress(
        confidence / 100
    )


    st.caption(
        """
This is a prototype risk/confidence indicator derived from
the magnitude of the detected deviation. It is not a
calibrated probability.
"""
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

The current observation differs significantly from the
normal sensor behaviour learned by the SKYGUARD monitoring
system.
"""
    )


    st.write(
        f"""
**Isolation Forest Anomaly Score:**
`{latest['anomaly_score']:.4f}`
"""
    )


# ============================================================
# TEMPERATURE GRAPH
# ============================================================

st.divider()

st.subheader(
    "🌡️ Temperature Monitoring"
)


temperature_fig = px.line(
    df,
    x="timestamp",
    y="temperature",
    title="Real-Time Temperature"
)


# Only highlight the CURRENT anomaly

if bool(latest["anomaly"]):

    temperature_fig.add_scatter(

        x=[latest["timestamp"]],

        y=[latest["temperature"]],

        mode="markers",

        name="🚨 Current Anomaly",

        marker=dict(
            size=14,
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

graph1, graph2 = st.columns(2)


with graph1:

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


# ============================================================
# PRESSURE GRAPH
# ============================================================

with graph2:

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


# ============================================================
# WIND GRAPH
# ============================================================

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

st.subheader(
    "📋 Event Log"
)


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
# CURRENT ANOMALY HISTORY
# ============================================================

st.divider()

st.subheader(
    "🚨 Current Anomaly Details"
)


if bool(latest["anomaly"]):

    anomaly_details = pd.DataFrame({

        "Parameter": [parameter],

        "Current Value": [
            f"{current_value:.2f} {unit}"
        ],

        "Expected Value": [
            f"{expected_value:.2f} {unit}"
        ],

        "Deviation": [
            f"{deviation:.2f} {unit}"
        ],

        "Status": [
            "🚨 ANOMALY"
        ]

    })


    st.dataframe(
        anomaly_details,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "🟢 No current anomaly detected."
    )


# ============================================================
# RAW DATA
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
                 WEATHER STATION
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Temperature     Humidity       Pressure
        │              │              │
        └──────────────┼──────────────┘
                       │
                  Wind Speed
                       │
                       ▼
                     ESP32
                       │
                     Wi-Fi
                       │
                       ▼
                SKYGUARD AI
                       │
                       ▼
              Data Processing
                       │
                       ▼
              Isolation Forest
                       │
              ┌────────┴────────┐
              │                 │
           NORMAL            ANOMALY
             🟢                 🚨
                               │
                               ▼
                       Fault Diagnosis
                               │
                               ▼
                        Expected Value
                               │
                               ▼
                         Explanation
                               │
                               ▼
                      Dashboard / Alert
""",
language="text"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    """
SKYGUARD AI • Intelligent Automatic Weather Station
Anomaly Detection • SIH Prototype
"""
)
