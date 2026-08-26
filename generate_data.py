import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# SKYGUARD AI - WEATHER DATA GENERATOR
# ==========================================

# Make random values repeatable
np.random.seed(42)

rows = []

# Start 24 hours ago
start_time = datetime.now() - timedelta(hours=24)


# ==========================================
# GENERATE NORMAL WEATHER DATA
# ==========================================

for i in range(1440):

    # One reading every minute
    timestamp = start_time + timedelta(minutes=i)

    # Normal temperature
    temperature = (
        28
        + np.sin(i / 120) * 3
        + np.random.normal(0, 0.5)
    )

    # Normal humidity
    humidity = (
        65
        - np.sin(i / 120) * 8
        + np.random.normal(0, 1.5)
    )

    # Normal pressure
    pressure = (
        1012
        + np.random.normal(0, 1)
    )

    # Normal wind speed
    wind_speed = max(
        0,
        5 + np.random.normal(0, 1.5)
    )

    rows.append([
        timestamp,
        "AWS-01",
        round(temperature, 2),
        round(humidity, 2),
        round(pressure, 2),
        round(wind_speed, 2)
    ])


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    rows,
    columns=[
        "timestamp",
        "station_id",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed"
    ]
)


# ==========================================
# INJECT FAKE SENSOR FAULT
# ==========================================

# Choose the reading where the fault will occur
fault_index = 1200

# Save the original temperature
normal_temperature = df.loc[
    fault_index,
    "temperature"
]

# Replace it with an abnormal temperature
df.loc[
    fault_index,
    "temperature"
] = 55.0


# ==========================================
# SAVE DATASET
# ==========================================

df.to_csv(
    "data/weather_data.csv",
    index=False
)


# ==========================================
# DISPLAY INFORMATION
# ==========================================

print()
print("========================================")
print("       SKYGUARD AI DATA GENERATOR")
print("========================================")

print()
print("✅ Weather dataset generated")
print(f"✅ Total records: {len(df)}")

print()
print("🚨 FAKE SENSOR FAULT INJECTED")

print(f"Station: AWS-01")
print(f"Fault index: {fault_index}")
print(f"Normal temperature: {normal_temperature:.2f} °C")
print(f"Fault temperature: 55.00 °C")

print()
print("📁 Dataset saved to:")
print("data/weather_data.csv")

print()
print("========================================")
print("           DATA GENERATION DONE")
print("========================================")