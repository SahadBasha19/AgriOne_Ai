import numpy as np

# Attempt to import TensorFlow; make it optional so the app can run
# in environments where TF is not installed. If TF is missing we
# keep `model` as None and surface a clear runtime error from
# `predict_disease()` asking the user to install TensorFlow.
try:
    import tensorflow as tf
except Exception as e:  # ImportError or other failures
    tf = None
    tf_import_error = str(e)

# -----------------------------------------
# Load Model (if TensorFlow is available)
# -----------------------------------------
MODEL_PATH = "models/disease_model.h5"

model = None
model_load_error = None

if tf is not None:
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        model_load_error = str(e)
else:
    model_load_error = (
        "TensorFlow is not available in this environment. "
        "Install it with: py -m pip install tensorflow"
    )

# -----------------------------------------
# Disease Classes
# -----------------------------------------

CLASS_NAMES = [
    "Apple Scab",
    "Apple Black Rot",
    "Apple Cedar Rust",
    "Healthy Apple",

    "Corn Cercospora Leaf Spot",
    "Corn Common Rust",
    "Corn Northern Leaf Blight",
    "Healthy Corn",

    "Potato Early Blight",
    "Potato Late Blight",
    "Healthy Potato",

    "Tomato Bacterial Spot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Septoria Leaf Spot",
    "Tomato Spider Mites",
    "Tomato Target Spot",
    "Tomato Mosaic Virus",
    "Tomato Yellow Leaf Curl Virus",
    "Healthy Tomato"
]

# -----------------------------------------
# Treatments
# -----------------------------------------

TREATMENTS = {

    "Apple Scab":
        "Apply fungicide and remove infected leaves.",

    "Apple Black Rot":
        "Prune infected branches and spray fungicide.",

    "Healthy Apple":
        "No treatment required.",

    "Potato Early Blight":
        "Use Mancozeb fungicide.",

    "Potato Late Blight":
        "Apply Copper fungicide immediately.",

    "Healthy Potato":
        "Healthy crop. Maintain irrigation.",

    "Healthy Tomato":
        "Healthy crop. Continue regular care."
}

# -----------------------------------------
# Prediction Function
# -----------------------------------------

def predict_disease(image):

    if model is None:
        raise RuntimeError(
            f"Disease model not loaded ({MODEL_PATH}). "
            f"{model_load_error or 'Please check the model file.'}"
        )

    prediction = model.predict(image)

    index = np.argmax(prediction)

    confidence = float(np.max(prediction))

    disease = CLASS_NAMES[index]

    treatment = TREATMENTS.get(
        disease,
        "Consult the nearest agriculture officer."
    )

    return {

        "disease": disease,

        "confidence": round(confidence * 100, 2),

        "treatment": treatment
    }
