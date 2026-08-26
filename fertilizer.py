import os

import joblib
import numpy as np
import streamlit as st

from utils.helper import page_header, footer


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = "models/fertilizer_model.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource(show_spinner=False)
def load_fertilizer_model():
    """
    Load the fertilizer model once and reuse it.
    """

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)

    except Exception as error:

        print(
            "Fertilizer Model Error:",
            error,
        )

        return None


# ============================================================
# CROP MAPPING
# ============================================================

CROP_MAP = {
    "Rice": 0,
    "Maize": 1,
    "Wheat": 2,
    "Cotton": 3,
    "Sugarcane": 4,
    "Groundnut": 5,
    "Potato": 6,
    "Tomato": 7,
}


# ============================================================
# FERTILIZER INFORMATION
# ============================================================

FERTILIZER_INFO = {

    "Urea":
        "Urea is a nitrogen-rich fertilizer that supports leafy "
        "vegetative growth.",

    "DAP":
        "DAP (Diammonium Phosphate) supplies nitrogen and "
        "phosphorus and is commonly used to support root development.",

    "MOP":
        "MOP (Muriate of Potash) supplies potassium, which supports "
        "overall crop development and quality.",

    "NPK":
        "NPK fertilizer supplies nitrogen, phosphorus, and potassium "
        "in a balanced formulation.",

    "Organic Compost":
        "Organic compost adds organic matter and can improve soil "
        "structure and nutrient availability.",

    "Vermicompost":
        "Vermicompost is an organic soil amendment that can improve "
        "soil fertility and structure.",
}


# ============================================================
# GENERAL TIPS
# ============================================================

FERTILIZER_TIPS = [
    "Apply fertilizer according to a soil test whenever possible.",
    "Avoid excessive fertilizer application.",
    "Follow the fertilizer product label for application instructions.",
    "Keep fertilizers away from water sources.",
    "Store fertilizers safely in a cool and dry place.",
]


# ============================================================
# CREATE MODEL FEATURES
# ============================================================

def create_features(
    nitrogen,
    phosphorus,
    potassium,
    moisture,
    crop,
):
    """
    Create features in the same order used by the original
    fertilizer model.
    """

    if crop not in CROP_MAP:
        raise ValueError(
            f"Unsupported crop: {crop}"
        )

    crop_value = CROP_MAP[crop]

    return np.array(
        [[
            nitrogen,
            phosphorus,
            potassium,
            moisture,
            crop_value,
        ]],
        dtype=float,
    )


# ============================================================
# PREDICTION
# ============================================================

def predict_fertilizer(
    model,
    features,
):
    """
    Generate fertilizer prediction.
    """

    prediction = model.predict(
        features
    )

    if prediction is None or len(prediction) == 0:

        raise ValueError(
            "The fertilizer model returned no prediction."
        )

    return str(
        prediction[0]
    )


# ============================================================
# CONFIDENCE
# ============================================================

def get_confidence(
    model,
    features,
):
    """
    Return confidence if the model supports predict_proba().
    """

    try:

        if not hasattr(
            model,
            "predict_proba",
        ):

            return None

        probabilities = model.predict_proba(
            features
        )

        probabilities = np.asarray(
            probabilities
        )

        if probabilities.size == 0:
            return None

        if probabilities.ndim > 1:
            probabilities = probabilities[0]

        return float(
            np.max(probabilities)
        )

    except Exception as error:

        print(
            "Fertilizer Confidence Error:",
            error,
        )

        return None


# ============================================================
# REPORT
# ============================================================

def create_report(
    crop,
    nitrogen,
    phosphorus,
    potassium,
    moisture,
    fertilizer,
    confidence,
):
    """

    Generate a downloadable fertilizer report.
    """

    if confidence is not None:

        confidence_text = (
            f"{confidence * 100:.2f}%"
        )

    else:

        confidence_text = (
            "Not available"
        )

    return f"""
========================================
             AGRIONE AI
      FERTILIZER RECOMMENDATION
========================================

Crop              : {crop}

Nitrogen (N)      : {nitrogen}
Phosphorus (P)    : {phosphorus}
Potassium (K)     : {potassium}
Soil Moisture     : {moisture} %

----------------------------------------
AI Recommendation
----------------------------------------

Recommended
Fertilizer        : {fertilizer}

Prediction
Confidence        : {confidence_text}

----------------------------------------
Important Tips
----------------------------------------

- Apply fertilizer according to soil-test results.
- Avoid excessive fertilizer application.
- Follow the product label.
- Keep fertilizers away from water sources.
- Store fertilizers safely.

========================================
Generated by AgriOne AI
========================================
"""


# ============================================================
# PAGE
# ============================================================

def app():

    page_header(
        "🧪 Fertilizer Recommendation"
    )

    st.write(
        "Enter soil nutrient values and crop details "
        "to receive an AI-based fertilizer recommendation."
    )

    st.info(
        "For accurate fertilizer dosage and application decisions, "
        "use a soil test and follow locally approved agricultural guidance."
    )

    st.divider()

    # --------------------------------------------------------
    # Load Model
    # --------------------------------------------------------

    model = load_fertilizer_model()

    if model is None:

        st.error(
            "The fertilizer model could not be loaded."
        )

        st.code(
            MODEL_PATH,
            language="text",
        )

        st.info(
            "Make sure fertilizer_model.pkl is inside "
            "the models folder."
        )

        footer()

        return

    # --------------------------------------------------------
    # Inputs
    # --------------------------------------------------------

    col1, col2 = st.columns(
        2
    )

    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0,
            max_value=300,
            value=90,
            step=1,
            key="fertilizer_nitrogen",
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0,
            max_value=300,
            value=45,
            step=1,
            key="fertilizer_phosphorus",
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0,
            max_value=300,
            value=40,
            step=1,
            key="fertilizer_potassium",
        )

    with col2:

        crop = st.selectbox(
            "🌾 Crop",
            list(
                CROP_MAP.keys()
            ),
            key="fertilizer_crop",
        )

        moisture = st.slider(
            "💧 Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=60,
            step=1,
            key="fertilizer_moisture",
        )

    st.divider()

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    if st.button(
        "🌱 Recommend Fertilizer",
        type="primary",
        use_container_width=True,
    ):

        try:

            features = create_features(
                nitrogen,
                phosphorus,
                potassium,
                moisture,
                crop,
            )

            with st.spinner(
                "🤖 Analyzing soil conditions..."
            ):

                fertilizer = predict_fertilizer(
                    model,
                    features,
                )

                confidence = get_confidence(
                    model,
                    features,
                )

            st.session_state[
                "fertilizer_result"
            ] = {

                "crop": crop,

                "nitrogen": nitrogen,

                "phosphorus": phosphorus,

                "potassium": potassium,

                "moisture": moisture,

                "fertilizer": fertilizer,

                "confidence": confidence,
            }

        except Exception as error:

            st.error(
                "Fertilizer recommendation failed."
            )

            st.exception(
                error
            )

            return

    # --------------------------------------------------------
    # Display Result
    # --------------------------------------------------------

    result = st.session_state.get(
        "fertilizer_result"
    )

    if result is None:

        st.info(
            "Enter the values above and click "
            "Recommend Fertilizer."
        )

        footer()

        return

    fertilizer = result[
        "fertilizer"
    ]

    confidence = result[
        "confidence"
    ]

    st.divider()

    st.subheader(
        "🧪 Recommendation"
    )

    result_col1, result_col2 = st.columns(
        2
    )

    with result_col1:

        st.success(
            "Recommendation generated successfully!"
        )

    with result_col2:

        st.metric(
            "Recommended Fertilizer",
            fertilizer,
        )

    # --------------------------------------------------------
    # Fertilizer Information
    # --------------------------------------------------------

    st.subheader(
        "📖 Fertilizer Information"
    )

    information = FERTILIZER_INFO.get(
        fertilizer,
        (
            "The AI model recommended this fertilizer. "
            "Check the product label and local agricultural "
            "guidance before application."
        ),
    )

    st.info(
        information
    )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    st.subheader(
        "📊 Prediction Confidence"
    )

    if confidence is not None:

        confidence_percentage = (
            confidence * 100
        )

        st.progress(
            min(
                max(
                    confidence,
                    0.0,
                ),
                1.0,
            )
        )

        st.metric(
            "Confidence",
            f"{confidence_percentage:.2f}%",
        )

        if confidence >= 0.80:

            st.success(
                "The model has relatively high confidence "
                "in this recommendation."
            )

        elif confidence >= 0.50:

            st.warning(
                "The model has moderate confidence. "
                "Consider confirming the recommendation."
            )

        else:

            st.warning(
                "The model confidence is low. "
                "Use this result only as an initial recommendation."
            )

    else:

        st.info(
            "This model does not provide probability scores."
        )

    # --------------------------------------------------------
    # Application Tips
    # --------------------------------------------------------

    st.subheader(
        "🌱 Application Tips"
    )

    for tip in FERTILIZER_TIPS:

        st.markdown(
            f"- ✅ {tip}"
        )

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Safety Tips"
    )

    st.warning(
        """
• Follow the fertilizer product label.

• Keep fertilizers away from children and animals.

• Keep fertilizers away from water sources.

• Avoid unnecessary mixing of fertilizer products.

• Use appropriate protective equipment when required.
"""
    )

    # --------------------------------------------------------
    # Input Summary
    # --------------------------------------------------------

    st.subheader(
        "🧪 Input Summary"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Crop",
            result["crop"],
        )

        st.metric(
            "Nitrogen",
            result["nitrogen"],
        )

    with col2:

        st.metric(
            "Phosphorus",
            result["phosphorus"],
        )

        st.metric(
            "Potassium",
            result["potassium"],
        )

    with col3:

        st.metric(
            "Moisture",
            f'{result["moisture"]}%',
        )

        st.metric(
            "Fertilizer",
            result["fertilizer"],
        )

    # --------------------------------------------------------
    # Download Report
    # --------------------------------------------------------

    st.subheader(
        "📄 Download Fertilizer Report"
    )

    report = create_report(
        result["crop"],
        result["nitrogen"],
        result["phosphorus"],
        result["potassium"],
        result["moisture"],
        result["fertilizer"],
        result["confidence"],
    )

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="AgriOne_AI_Fertilizer_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Clear Result
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Recommendation",
        use_container_width=True,
    ):

        st.session_state.pop(
            "fertilizer_result",
            None,
        )

        st.rerun()

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.markdown("---")

    st.success(
        "🌱 Balanced fertilizer management can support "
        "healthy crop growth and soil health."
    )

    footer()