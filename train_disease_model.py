import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os


# -----------------------------
# Dataset Path
# -----------------------------

DATASET_PATH = "dataset/PlantVillage"


IMAGE_SIZE = 224
BATCH_SIZE = 32


# -----------------------------
# Image Preprocessing
# -----------------------------

datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,

    rotation_range=20,

    zoom_range=0.2,

    horizontal_flip=True

)


train_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMAGE_SIZE, IMAGE_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training"

)


validation_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMAGE_SIZE, IMAGE_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation"

)


# -----------------------------
# CNN Model
# -----------------------------

model = Sequential()


model.add(
    Conv2D(
        32,
        (3,3),
        activation="relu",
        input_shape=(224,224,3)
    )
)

model.add(MaxPooling2D())


model.add(
    Conv2D(
        64,
        (3,3),
        activation="relu"
    )
)

model.add(MaxPooling2D())


model.add(
    Conv2D(
        128,
        (3,3),
        activation="relu"
    )
)

model.add(MaxPooling2D())


model.add(Flatten())


model.add(
    Dense(
        128,
        activation="relu"
    )
)


model.add(
    Dropout(0.5)
)


model.add(
    Dense(
        train_data.num_classes,
        activation="softmax"
    )
)


# -----------------------------
# Compile
# -----------------------------

model.compile(

    optimizer=Adam(
        learning_rate=0.0001
    ),

    loss="categorical_crossentropy",

    metrics=["accuracy"]

)


# -----------------------------
# Train
# -----------------------------

history = model.fit(

    train_data,

    validation_data=validation_data,

    epochs=10

)


# -----------------------------
# Save Model
# -----------------------------

os.makedirs(
    "models",
    exist_ok=True
)


model.save(
    "models/disease_model.h5"
)


print(
    "✅ Disease model saved successfully"
)