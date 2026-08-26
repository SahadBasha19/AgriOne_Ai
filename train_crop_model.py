import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -----------------------------
# Load Dataset
# -----------------------------

DATASET_PATH = "dataset/crop_recommendation.csv"

df = pd.read_csv(DATASET_PATH)


# -----------------------------
# Split Features and Target
# -----------------------------

X = df.drop("label", axis=1)

y = df["label"]


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
# Model Training
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
# Evaluation
# -----------------------------

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)


print(
    f"Crop Model Accuracy: {accuracy*100:.2f}%"
)


# -----------------------------
# Save Model
# -----------------------------

MODEL_PATH = "models/crop_model.pkl"

joblib.dump(

    model,

    MODEL_PATH

)


print(
    "✅ crop_model.pkl saved successfully"
)