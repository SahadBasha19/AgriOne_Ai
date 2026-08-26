from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -------------------------------
# App Settings
# -------------------------------
APP_NAME = "AgriOne AI"
APP_VERSION = "1.0"

# -------------------------------
# Languages
# -------------------------------
LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta"
}

DEFAULT_LANGUAGE = "English"

# -------------------------------
# Assets
# -------------------------------
LOGO = "assets/logo.png"
BACKGROUND = "assets/background.jpg"
LOTTIE_FILE = "assets/loading.json"

# -------------------------------
# Dataset
# -------------------------------
SCHEME_FILE = "dataset/schemes.csv"

# -------------------------------
# Models
# -------------------------------
CROP_MODEL = "models/crop_model.pkl"
FERTILIZER_MODEL = "models/fertilizer_model.pkl"
DISEASE_MODEL = "models/disease_model.h5"
