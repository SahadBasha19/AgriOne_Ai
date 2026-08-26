import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


# -----------------------------
# Load Dataset
# -----------------------------

DATASET_PATH = "dataset/fertilizer.csv"

df = pd.read_csv(DATASET_PATH)


# -----------------------------
# Encode Categorical Columns
# -----------------------------

soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()


df["Soil_Type"] = soil_encoder.fit_transform(
    df["Soil_Type"]
)

df["Crop_Type"] = crop_encoder.fit_transform(
    df["Crop_Type"]
)


# -----------------------------
# Features and Target
# -----------------------------

X = df.drop(
    "Fertilizer_Name",
    axis=1
)

y = df["Fertilizer_Name"]


# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)


# -----------------------------
# Train Model
# -----------------------------

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)


model.fit(

    X_train,

    y_train

)


# -----------------------------
# Accuracy
# -----------------------------

prediction = model.predict(
    X_test
)


accuracy = accuracy_score(

    y_test,

    prediction

)


print(
    f"Fertilizer Model Accuracy: {accuracy*100:.2f}%"
)


# -----------------------------
# Save Model
# -----------------------------

joblib.dump(

    model,

    "models/fertilizer_model.pkl"

)


# Save Encoders

joblib.dump(

    soil_encoder,

    "models/soil_encoder.pkl"

)

joblib.dump(

    crop_encoder,

    "models/crop_encoder.pkl"

)


print(
    "✅ Fertilizer model saved successfully"
)