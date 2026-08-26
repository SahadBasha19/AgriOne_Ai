import os

import joblib
import numpy as np
import streamlit as st

from utils.helper import page_header, footer


# ============================================================
# CROP MODEL
# ============================================================

MODEL_PATH = "models/crop_model.pkl"


@st.cache_resource(show_spinner=False)
def load_crop_model():
    """
    Load the crop recommendation model only once.

    Streamlit reruns the application frequently, so caching the
    model prevents joblib from loading the file repeatedly.
    """

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)

    except Exception as error:
        print(
            "Crop Model Error:",
            error,
        )
        return None


# ============================================================
# CROP INFORMATION
# ============================================================

CROP_INFO = {

    "rice":
        "Rice grows well in warm climates with high rainfall "
        "and fertile soil.",

    "maize":
        "Maize requires well-drained soil and moderate rainfall.",

    "cotton":
        "Cotton grows best in black soil with warm temperatures.",

    "wheat":
        "Wheat prefers cool climates and fertile loamy soil.",

    "potato":
        "Potatoes grow well in cool weather with loose, "
        "well-drained soil.",

    "sugarcane":
        "Sugarcane requires warm temperatures and abundant water.",

    "groundnut":
        "Groundnut prefers sandy loam soil and moderate rainfall.",

}


# ============================================================
# CROP TIPS
# ============================================================

CROP_TIPS = [

    "Use certified quality seeds.",

    "Maintain proper irrigation.",

    "Test soil before applying fertilizers.",

    "Monitor pests regularly.",

    "Harvest at the correct maturity stage.",

]


# ============================================================
# CREATE FEATURES
# ============================================================

def create_features(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
):
    """
    Create the feature array in the same order expected by
    the original crop model.
    """

    return np.array(
        [[
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
        ]],
        dtype=float,
    )


# ============================================================
# CROP PREDICTION
# ============================================================

def predict_crop(
    model,
    features,
):
    """
    Generate crop prediction.
    """

    prediction = model.predict(
        features
    )

    if prediction is None or len(prediction) == 0:
        raise ValueError(
            "The crop model did not return a prediction."
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
    Get prediction confidence when the trained model supports
    predict_proba().
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

        if probabilities is None:
            return None

        probabilities = np.asarray(
            probabilities
        )

        if probabilities.size == 0:
            return None

        if probabilities.ndim > 1:
            probabilities = probabilities[0]

        confidence = float(
            np.max(probabilities)
        )

        return confidence

    except Exception as error:

        print(
            "Confidence Error:",
            error,
        )

        return None


# ============================================================
# REPORT
# ============================================================

def create_report(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
    crop,
    confidence,
):
    """
    Create downloadable crop recommendation report.
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
      CROP RECOMMENDATION REPORT
========================================

Soil & Weather Information
----------------------------------------

Nitrogen       : {nitrogen}
Phosphorus     : {phosphorus}
Potassium      : {potassium}
Temperature    : {temperature} °C
Humidity       : {humidity} %
Soil pH        : {ph}
Rainfall       : {rainfall} mm

----------------------------------------
AI Recommendation
----------------------------------------

Recommended Crop : {crop}

Prediction Confidence : {confidence_text}

----------------------------------------
General Growing Tips
----------------------------------------

- Use certified quality seeds.
- Maintain proper irrigation.
- Test soil before applying fertilizers.
- Monitor pests regularly.
- Harvest at the correct maturity stage.

========================================
Generated by AgriOne AI
========================================
"""


# ============================================================
# PAGE
# ============================================================

def app():

    page_header(
        "🌾 AI Crop Recommendation"
    )

    st.write(
        "Enter your soil and weather details to get "
        "the most suitable crop recommendation."
    )

    st.info(
        "The recommendation is an AI-based prediction. "
        "For important farming decisions, consider local "
        "soil tests and agricultural guidance."
    )

    st.divider()

    # --------------------------------------------------------
    # Load Model
    # --------------------------------------------------------

    model = load_crop_model()

    if model is None:

        st.error(
            "Crop model not found or could not be loaded."
        )

        st.code(
            "models/crop_model.pkl",
            language="text",
        )

        st.info(
            "Place your trained crop_model.pkl file "
            "inside the models folder."
        )

        footer()

        return

    # --------------------------------------------------------
    # Input Fields
    # --------------------------------------------------------

    col1, col2 = st.columns(
        2
    )

    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=300.0,
            value=90.0,
            step=1.0,
            key="crop_nitrogen",
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=300.0,
            value=42.0,
            step=1.0,
            key="crop_phosphorus",
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=300.0,
            value=43.0,
            step=1.0,
            key="crop_potassium",
        )

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=60.0,
            value=28.0,
            step=0.1,
            key="crop_temperature",
        )

    with col2:

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=0.1,
            key="crop_humidity",
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1,
            key="crop_ph",
        )

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=500.0,
            value=180.0,
            step=1.0,
            key="crop_rainfall",
        )

    st.divider()

    # --------------------------------------------------------
    # Recommend Crop
    # --------------------------------------------------------

    if st.button(
        "🌱 Recommend Crop",
        type="primary",
        use_container_width=True,
    ):

        try:

            features = create_features(
                nitrogen,
                phosphorus,
                potassium,
                temperature,
                humidity,
                ph,
                rainfall,
            )

            with st.spinner(
                "🤖 Analyzing soil and weather conditions..."
            ):

                crop = predict_crop(
                    model,
                    features,
                )

                confidence = get_confidence(
                    model,
                    features,
                )

            # Save result
            st.session_state[
                "crop_result"
            ] = {
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall,
                "crop": crop,
                "confidence": confidence,
            }

        except Exception as error:

            st.error(
                "Crop recommendation failed."
            )

            st.exception(
                error
            )

            return

    # --------------------------------------------------------
    # Display Saved Result
    # --------------------------------------------------------

    result = st.session_state.get(
        "crop_result"
    )

    if result is None:

        st.info(
            "Enter the values above and click "
            "Recommend Crop."
        )

        footer()

        return

    crop = result["crop"]

    confidence = result[
        "confidence"
    ]

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🌾 Recommendation"
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
            "Recommended Crop",
            crop,
        )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    if confidence is not None:

        st.subheader(
            "📊 Prediction Confidence"
        )

        percentage = (
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
            f"{percentage:.2f}%",
        )

        if confidence >= 0.80:

            st.success(
                "The model has relatively high confidence "
                "in this recommendation."
            )

        elif confidence >= 0.50:

            st.warning(
                "The model has moderate confidence. "
                "Consider additional soil and local conditions."
            )

        else:

            st.warning(
                "The model confidence is low. "
                "Use this result only as an initial recommendation."
            )

    else:

        st.info(
            "This trained model does not provide probability scores."
        )

    # --------------------------------------------------------
    # Crop Information
    # --------------------------------------------------------

    st.subheader(
        "📖 Crop Information"
    )

    crop_key = crop.strip().lower()

    info = CROP_INFO.get(
        crop_key,
        "This crop was recommended by the AI model. "
        "Check its local growing requirements before planting.",
    )

    st.info(
        info
    )

    # --------------------------------------------------------
    # Growing Tips
    # --------------------------------------------------------

    st.subheader(
        "🌱 Growing Tips"
    )

    for tip in CROP_TIPS:

        st.markdown(
            f"- ✅ {tip}"
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
            "Nitrogen",
            f'{result["nitrogen"]:.1f}',
        )

        st.metric(
            "Temperature",
            f'{result["temperature"]:.1f} °C',
        )

        st.metric(
            "Rainfall",
            f'{result["rainfall"]:.1f} mm',
        )

    with col2:

        st.metric(
            "Phosphorus",
            f'{result["phosphorus"]:.1f}',
        )

        st.metric(
            "Humidity",
            f'{result["humidity"]:.1f}%',
        )

    with col3:

        st.metric(
            "Potassium",
            f'{result["potassium"]:.1f}',
        )

        st.metric(
            "Soil pH",
            f'{result["ph"]:.1f}',
        )

    # --------------------------------------------------------
    # Download Report
    # --------------------------------------------------------

    st.subheader(
        "📄 Download Report"
    )

    report = create_report(
        result["nitrogen"],
        result["phosphorus"],
        result["potassium"],
        result["temperature"],
        result["humidity"],
        result["ph"],
        result["rainfall"],
        result["crop"],
        result["confidence"],
    )

    st.download_button(
        label="📥 Download Recommendation",
        data=report,
        file_name="AgriOne_AI_Crop_Recommendation.txt",
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
            "crop_result",
            None,
        )

        st.rerun()

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.markdown("---")

    st.success(
        "🌾 Choosing the right crop can help improve "
        "farm planning and productivity."
    )

    footer()