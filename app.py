
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Chennai Weather AI",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Chennai AI Weather Dashboard")
st.caption("Powered by Open-Meteo")

# Fetch forecast
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m"
    ],
    "forecast_days": 3,
    "timezone": "Asia/Kolkata"
}

try:
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data["hourly"])

    st.success("Weather data loaded successfully!")

    st.subheader("Next 72 Hours")

    st.line_chart(
        df.set_index("time")["temperature_2m"]
    )

    st.line_chart(
        df.set_index("time")["relative_humidity_2m"]
    )

    st.bar_chart(
        df.set_index("time")["precipitation"]
    )

    st.line_chart(
        df.set_index("time")["wind_speed_10m"]
    )

    st.subheader("Hourly Weather Data")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Unable to load weather data: {e}")
