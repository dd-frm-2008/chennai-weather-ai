
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Chennai Weather AI",
    page_icon="🌦️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071526, #102b49);
    color: #FFFFFF;
}
h1, h2, h3 {
    color: #FFFFFF !important;
}
p, label, span {
    color: #B8D8EA;
}
[data-testid="stMetric"] {
    background: #193653;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #315475;
}
[data-testid="stMetricValue"] {
    color: #61D4FF;
}
[data-testid="stMetricLabel"] {
    color: #B8D8EA;
}
</style>
""", unsafe_allow_html=True)

st.title("🌦️ CHENNAI WEATHER AI")
st.caption("Your 72-hour weather dashboard | Chennai, Tamil Nadu")

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

@st.cache_data(ttl=1800)
def get_weather():
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return pd.DataFrame(response.json()["hourly"])

try:
    df = get_weather()
    df["time"] = pd.to_datetime(df["time"])

    now = pd.Timestamp.now()
    df = df[df["time"] >= now.floor("h")].copy()

    if df.empty:
        st.warning("No upcoming forecast data available.")
        st.stop()

    st.success("Live forecast loaded successfully")

    # WEATHER OVERVIEW
    st.subheader("📊 Weather Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡️ Temperature",
                f"{df['temperature_2m'].iloc[0]:.1f} °C")
    col2.metric("💧 Humidity",
                f"{df['relative_humidity_2m'].iloc[0]:.0f}%")
    col3.metric("💨 Wind Speed",
                f"{df['wind_speed_10m'].iloc[0]:.1f} km/h")
    col4.metric("🌧️ Rainfall",
                f"{df['precipitation'].iloc[0]:.1f} mm")

    st.divider()

    # TEMPERATURE GRAPH
    st.subheader("🌡️ Temperature Forecast")

    fig1 = px.line(
        df, x="time", y="temperature_2m",
        markers=True,
        labels={
            "time": "Time",
            "temperature_2m": "Temperature (°C)"
        }
    )

    fig1.update_traces(
        line=dict(color="#FFB74D", width=3),
        marker=dict(size=7)
    )

    # HUMIDITY GRAPH
    st.subheader("💧 Humidity Forecast")

    fig2 = px.line(
        df, x="time", y="relative_humidity_2m",
        markers=True,
        labels={"relative_humidity_2m": "Humidity (%)"}
    )

    fig2.update_traces(
        line=dict(color="#29B6F6", width=3),
        marker=dict(size=7)
    )

    # WIND SPEED GRAPH
    st.subheader("💨 Wind Speed Forecast")

    fig3 = px.line(
        df, x="time", y="wind_speed_10m",
        markers=True,
        labels={"wind_speed_10m": "Wind Speed (km/h)"}
    )

    fig3.update_traces(
        line=dict(color="#AB83FF", width=3),
        marker=dict(size=7)
    )

    # RAINFALL GRAPH
    st.subheader("🌧️ Rainfall Forecast")

    fig4 = px.bar(
        df, x="time", y="precipitation",
        labels={"precipitation": "Rainfall (mm)"}
    )

    fig4.update_traces(
        marker_color="#00DFA2",
        marker_line_width=0
    )

    # COMMON GRAPH STYLING
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            template="plotly_dark",
            font=dict(color="#FFFFFF", size=13),
            xaxis=dict(
                title_font=dict(color="#8BE3FF"),
                tickfont=dict(color="#FFFFFF")
            ),
            yaxis=dict(
                title_font=dict(color="#8BE3FF"),
                tickfont=dict(color="#FFFFFF")
            )
        )

    # DISPLAY GRAPHS
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.plotly_chart(fig3, use_container_width=True)

    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # HOURLY FORECAST TABLE
    st.subheader("🕒 Hourly Weather Forecast")

    display_df = df.rename(columns={
        "time": "Time",
        "temperature_2m": "Temperature (°C)",
        "relative_humidity_2m": "Humidity (%)",
        "precipitation": "Rainfall (mm)",
        "wind_speed_10m": "Wind Speed (km/h)"
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Weather forecast data provided by Open-Meteo. "
        "This dashboard displays forecast data, not ML predictions."
    )

    st.caption(
        f"Last refreshed: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

except Exception as e:
    st.error(f"Unable to load weather data: {e}")
