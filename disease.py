# ============================================================
# AgriOne AI - Crop Disease Detection
# Image + PDF Upload + Gemini AI
# ============================================================

import os
import streamlit as st

# ------------------------------------------------------------
# TRANSLATION
# ------------------------------------------------------------

try:
    from utils.i18n import t
except Exception:

    def t(key, default=None, language=None):
        return default or key


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

try:
    from config import GEMINI_API_KEY, MODEL_NAME
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash"
    )


# ------------------------------------------------------------
# GEMINI NEW SDK
# ------------------------------------------------------------

try:
    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True

except ImportError:

    genai = None
    types = None
    GEMINI_AVAILABLE = False


# ------------------------------------------------------------
# GEMINI CLIENT
# ------------------------------------------------------------

def get_client():

    if not GEMINI_AVAILABLE:
        return None

    if not GEMINI_API_KEY:
        return None

    try:

        return genai.Client(
            api_key=GEMINI_API_KEY
        )

    except Exception:

        return None


# ------------------------------------------------------------
# DISEASE PROMPT
# ------------------------------------------------------------

def create_prompt(language):

    return f"""
You are AgriOne AI, an agricultural crop disease assistant.

Analyze the uploaded crop image, leaf image, or agricultural PDF.

IMPORTANT:
- Reply ONLY in {language}.
- Use simple language suitable for farmers.
- Do not invent information.
- If the image/document is unclear, say so.
- Do not claim certainty when the evidence is insufficient.
- Give practical and safe agricultural guidance.
- Avoid unsafe pesticide or chemical dosage instructions.

Return the answer using these sections:

CROP
Identify the crop if possible.

DISEASE / CONDITION
Give the most likely disease or condition.

CONFIDENCE
Low / Medium / High.

SYMPTOMS
Explain the visible or documented symptoms.

POSSIBLE CAUSES
Explain likely causes.

MANAGEMENT
Give practical management suggestions.

PREVENTION
Give prevention steps.

WHEN TO SEEK EXPERT HELP
Explain when the farmer should contact a local agricultural officer,
agronomist, or plant pathologist.

If the uploaded file is not related to crops/agriculture,
clearly explain that it cannot be used for disease detection.
"""


# ------------------------------------------------------------
# GEMINI ANALYSIS
# ------------------------------------------------------------

def analyze_file(uploaded_file, language):

    client = get_client()

    if client is None:

        if not GEMINI_AVAILABLE:

            return (
                None,
                "Gemini package is missing. "
                "Run: pip install -U google-genai"
            )

        return (
            None,
            "Gemini API key is missing. "
            "Please check GEMINI_API_KEY in your .env file."
        )

    try:

        file_bytes = uploaded_file.getvalue()

        mime_type = uploaded_file.type

        if not mime_type:

            mime_type = "application/octet-stream"

        prompt = create_prompt(
            language
        )

        file_part = types.Part.from_bytes(
            data=file_bytes,
            mime_type=mime_type
        )

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=[
                prompt,
                file_part
            ]
        )

        answer = getattr(
            response,
            "text",
            None
        )

        if answer:

            return (
                answer.strip(),
                None
            )

        return (
            None,
            "Gemini did not return an analysis."
        )

    except Exception as error:

        error_text = str(error)

        print(
            "Disease Detection Error:",
            error_text
        )

        if "429" in error_text:

            return (
                None,
                "Gemini usage limit reached. "
                "Please try again later."
            )

        if "401" in error_text or "403" in error_text:

            return (
                None,
                "Gemini API authentication failed. "
                "Please check your GEMINI_API_KEY."
            )

        if "404" in error_text:

            return (
                None,
                f"Gemini model '{MODEL_NAME}' was not found. "
                "Please check MODEL_NAME in config.py."
            )

        return (
            None,
            f"Could not analyze the uploaded file.\n\n"
            f"Error: {error_text}"
        )


# ------------------------------------------------------------
# RESULT DISPLAY
# ------------------------------------------------------------

def show_result(result):

    st.markdown("---")

    st.subheader(
        "🤖 AI Disease Analysis"
    )

    st.markdown(
        result
    )

    st.success(
        "🌱 Use this result as an AI-assisted indication. "
        "For serious crop damage, consult a local agricultural expert."
    )


# ------------------------------------------------------------
# MAIN PAGE
# ------------------------------------------------------------

def app():

    language = st.session_state.get(
        "language",
        "English"
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "🌿 AI Crop Disease Detection"
    )

    st.write(
        "Upload a crop/leaf image or an agricultural PDF "
        "and let AgriOne AI analyze it."
    )

    # ========================================================
    # SUPPORTED FILES
    # ========================================================

    st.info(
        "📁 Supported files: "
        "JPG • JPEG • PNG • WEBP • PDF"
    )

    # ========================================================
    # UPLOAD
    # ========================================================

    uploaded_file = st.file_uploader(

        "📤 Upload Crop Image or PDF",

        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "pdf"
        ],

        key="disease_detector_upload"
    )

    # ========================================================
    # NO FILE
    # ========================================================

    if uploaded_file is None:

        st.markdown(
            """
            ### 🔬 How it works

            1. Upload a clear crop or leaf image.
            2. Or upload an agricultural PDF.
            3. Select your language from the sidebar.
            4. Click **Analyze Disease**.
            5. Gemini AI provides the analysis.
            """
        )

        return

    # ========================================================
    # FILE INFORMATION
    # ========================================================

    st.success(
        f"✅ Uploaded: {uploaded_file.name}"
    )

    file_size_mb = (
        len(uploaded_file.getvalue())
        / (1024 * 1024)
    )

    st.caption(
        f"File type: {uploaded_file.type or 'Unknown'} "
        f"• Size: {file_size_mb:.2f} MB"
    )

    # ========================================================
    # IMAGE PREVIEW
    # ========================================================

    if uploaded_file.type in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:

        st.image(
            uploaded_file,
            caption="🌱 Uploaded Crop Image",
            use_container_width=True
        )

    # ========================================================
    # PDF
    # ========================================================

    elif uploaded_file.type == "application/pdf":

        st.info(
            "📄 PDF uploaded successfully. "
            "Gemini AI will analyze the document."
        )

    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    if st.button(

        "🔍 Analyze Disease",

        type="primary",

        use_container_width=True,

        key="analyze_crop_disease"

    ):

        with st.spinner(
            "🤖 AgriOne AI is analyzing your file..."
        ):

            result, error = analyze_file(
                uploaded_file,
                language
            )

        if error:

            st.error(
                error
            )

        else:

            show_result(
                result
            )


# ------------------------------------------------------------
# IMPORTANT
# ------------------------------------------------------------

# Do NOT put st.set_page_config() here.
# app.py already controls the application configuration.