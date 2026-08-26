import os
import tempfile

import streamlit as st
from gtts import gTTS

from utils.weather_api import get_weather, farming_advice
from utils.helper import page_header, footer


# ============================================================
# WEATHER PAGE
# ============================================================

def app():

    page_header("🌤 Live Weather Forecast")

    st.write(
        "Check current weather conditions and get "
        "simple farming advice."
    )

    st.divider()

    # --------------------------------------------------------
    # City Input
    # --------------------------------------------------------

    city = st.text_input(
        "📍 Enter City Name",
        placeholder="Example: Hyderabad",
        key="weather_city",
    )

    get_weather_button = st.button(
        "🌦 Get Weather",
        type="primary",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Fetch Weather
    # --------------------------------------------------------

    if get_weather_button:

        city = city.strip()

        if not city:

            st.warning(
                "Please enter a city name."
            )

            return

        with st.spinner(
            "🌤 Fetching latest weather..."
        ):

            result = get_weather(
                city
            )

        if not result.get("success"):

            st.error(
                result.get(
                    "message",
                    "Unable to fetch weather information.",
                )
            )

            return

        # Save result so it remains visible after
        # other Streamlit interactions.
        st.session_state[
            "weather_result"
        ] = result

    # --------------------------------------------------------
    # Existing Result
    # --------------------------------------------------------

    result = st.session_state.get(
        "weather_result"
    )

    if not result:

        st.info(
            "Enter a city name and click "
            "Get Weather to view the latest conditions."
        )

        st.markdown("---")

        st.info(
            "🌦 Always check weather conditions before "
            "irrigation, spraying, or harvesting."
        )

        footer()

        return

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    st.subheader(
        "🌍 Location"
    )

    location_col1, location_col2 = st.columns(
        2
    )

    with location_col1:

        st.write(
            f"**City:** {result.get('city', 'Unknown')}"
        )

    with location_col2:

        st.write(
            f"**Country:** {result.get('country', 'Unknown')}"
        )

    st.success(
        "Weather information loaded successfully!"
    )

    # --------------------------------------------------------
    # Weather Details
    # --------------------------------------------------------

    st.subheader(
        "🌡 Weather Details"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        temperature = result.get(
            "temperature",
            "N/A",
        )

        if isinstance(
            temperature,
            (int, float),
        ):

            temperature_text = (
                f"{temperature:.1f} °C"
            )

        else:

            temperature_text = (
                f"{temperature} °C"
            )

        st.metric(
            "Temperature",
            temperature_text,
        )

    with col2:

        feels_like = result.get(
            "feels_like",
            "N/A",
        )

        if isinstance(
            feels_like,
            (int, float),
        ):

            feels_like_text = (
                f"{feels_like:.1f} °C"
            )

        else:

            feels_like_text = (
                f"{feels_like} °C"
            )

        st.metric(
            "Feels Like",
            feels_like_text,
        )

    with col3:

        humidity = result.get(
            "humidity",
            "N/A",
        )

        st.metric(
            "Humidity",
            f"{humidity} %",
        )

    col4, col5, col6 = st.columns(
        3
    )

    with col4:

        st.metric(
            "Pressure",
            f"{result.get('pressure', 'N/A')} hPa",
        )

    with col5:

        st.metric(
            "Wind Speed",
            f"{result.get('wind_speed', 'N/A')} m/s",
        )

    with col6:

        st.metric(
            "Condition",
            result.get(
                "description",
                "Unknown",
            ),
        )

    # --------------------------------------------------------
    # Weather Icon
    # --------------------------------------------------------

    icon = result.get(
        "icon"
    )

    if icon:

        icon_url = (
            "https://openweathermap.org/img/wn/"
            f"{icon}@2x.png"
        )

        icon_col1, icon_col2, icon_col3 = st.columns(
            [1, 1, 1]
        )

        with icon_col2:

            try:

                st.image(
                    icon_url,
                    width=100,
                )

            except Exception:

                pass

    # --------------------------------------------------------
    # Farming Advice
    # --------------------------------------------------------

    st.subheader(
        "🌾 Farming Advice"
    )

    temperature = result.get(
        "temperature"
    )

    humidity = result.get(
        "humidity"
    )

    if (
        isinstance(temperature, (int, float))
        and isinstance(humidity, (int, float))
    ):

        advice = farming_advice(
            temperature,
            humidity,
        )

    else:

        advice = result.get(
            "advice",
            "Follow local agricultural guidance based on current weather.",
        )

    st.success(
        advice
    )

    # --------------------------------------------------------
    # Voice Weather Report
    # --------------------------------------------------------

    st.subheader(
        "🔊 Voice Weather Report"
    )

    st.write(
        "Generate an audio summary of the current weather."
    )

    if st.button(
        "🔊 Read Weather",
        key="weather_voice",
        use_container_width=True,
    ):

        city_name = result.get(
            "city",
            "your location",
        )

        description = result.get(
            "description",
            "unknown conditions",
        )

        summary = (
            f"Weather in {city_name}. "
            f"Temperature is {temperature} degrees Celsius. "
            f"Humidity is {humidity} percent. "
            f"Weather condition is {description}. "
            f"{advice}"
        )

        temp_path = None

        try:

            with st.spinner(
                "🔊 Preparing voice report..."
            ):

                tts = gTTS(
                    summary,
                    lang="en",
                    slow=False,
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3",
                ) as temp_file:

                    temp_path = temp_file.name

                tts.save(
                    temp_path
                )

            with open(
                temp_path,
                "rb",
            ) as audio_file:

                audio_data = audio_file.read()

            st.audio(
                audio_data,
                format="audio/mp3",
            )

        except Exception as error:

            st.error(
                f"Unable to create voice report: {error}"
            )

        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                try:

                    os.remove(
                        temp_path
                    )

                except Exception:

                    pass

    # --------------------------------------------------------
    # Download Weather Report
    # --------------------------------------------------------

    st.subheader(
        "📄 Weather Report"
    )

    report = f"""
========================================
          AGRIONE AI
       WEATHER REPORT
========================================

City          : {result.get('city', 'N/A')}
Country       : {result.get('country', 'N/A')}

Temperature   : {temperature} °C
Feels Like    : {result.get('feels_like', 'N/A')} °C
Humidity      : {humidity} %
Pressure      : {result.get('pressure', 'N/A')} hPa
Wind Speed    : {result.get('wind_speed', 'N/A')} m/s
Condition     : {result.get('description', 'N/A')}

Farming Advice:
{advice}

========================================
Generated by AgriOne AI
========================================
"""

    st.download_button(
        label="📥 Download Weather Report",
        data=report,
        file_name="AgriOne_AI_Weather_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Clear Weather
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Weather",
        key="clear_weather",
        use_container_width=True,
    ):

        st.session_state.pop(
            "weather_result",
            None,
        )

        st.rerun()

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.markdown("---")

    st.info(
        "🌦 Always check weather conditions before "
        "irrigation, spraying, or harvesting."
    )

    footer()