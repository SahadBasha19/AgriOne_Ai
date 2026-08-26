import numpy as np
from PIL import Image


# -----------------------------------
# Image Size
# -----------------------------------
IMAGE_SIZE = (224, 224)


# -----------------------------------
# Load Image
# -----------------------------------
def load_image(uploaded_file):

    image = Image.open(uploaded_file)

    image = image.convert("RGB")

    return image


# -----------------------------------
# Resize Image
# -----------------------------------
def resize_image(image):

    image = image.resize(IMAGE_SIZE)

    return image


# -----------------------------------
# Convert to NumPy
# -----------------------------------
def image_to_array(image):

    img = np.array(image)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img


# -----------------------------------
# Complete Preprocessing
# -----------------------------------
def preprocess(uploaded_file):

    image = load_image(uploaded_file)

    resized = resize_image(image)

    img_array = image_to_array(resized)

    return image, img_array
