import streamlit as st  # type: ignore
from api import get_weather_status


def render_weather_info():
    weather = get_weather_status()

    if "error" in weather:
        st.error(f"Weather fetch error: {weather['error']}")
        return

    icon = "🌞" if weather["time_of_day"] == "day" else "🌙"
    st.markdown(f"### {icon} Weather Now: "
                f"{weather['weatherDesc']} - {weather['temp_C']}°C")
