import streamlit as st
from PIL import Image
import base64
import os
import random

# ----------------------------
# Load Image
# ----------------------------
def load_image(path):

    try:
        return Image.open(path)

    except:
        return None


# ----------------------------
# Display Logo
# ----------------------------
def show_logo(path="assets/logo.png"):

    if os.path.exists(path):
        st.image(path, width=120)


# ----------------------------
# Encode Image
# ----------------------------
def get_base64(file_path):

    with open(file_path, "rb") as file:

        data = base64.b64encode(file.read()).decode()

    return data


# ----------------------------
# Success Message
# ----------------------------
def success(message):

    st.success(message)


# ----------------------------
# Error Message
# ----------------------------
def error(message):

    st.error(message)


# ----------------------------
# Warning Message
# ----------------------------
def warning(message):

    st.warning(message)


# ----------------------------
# Daily Farming Tips
# ----------------------------
def farming_tip():

    tips = [

        "🌱 Test soil before planting crops.",

        "💧 Water crops early morning.",

        "🌿 Remove weeds every week.",

        "🧪 Apply fertilizers only after soil testing.",

        "🌾 Rotate crops every season.",

        "🌤 Monitor weather before irrigation.",

        "🐞 Check plants daily for insects.",

        "🍅 Remove infected leaves immediately.",

        "🌳 Use organic compost whenever possible.",

        "🚜 Maintain farm equipment regularly."

    ]

    return random.choice(tips)


# ----------------------------
# Header
# ----------------------------
def page_header(title):

    st.markdown(
        f"""
        <h1 style='color:green;text-align:center;'>
        {title}
        </h1>
        """,
        unsafe_allow_html=True
    )


# ----------------------------
# Footer
# ----------------------------
def footer():

    st.markdown("---")

    st.markdown(
        """
<center>

🌾 AgriOne AI

Made for Smart Farmers ❤️

</center>
""",
        unsafe_allow_html=True
    )


# ----------------------------
# Confidence Color
# ----------------------------
def confidence_color(value):

    if value >= 90:
        return "green"

    elif value >= 70:
        return "orange"

    return "red"
