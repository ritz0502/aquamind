import os
import io
import json
import numpy as np
from flask import Blueprint, request, jsonify
from PIL import Image
import tensorflow as tf

coral_bp = Blueprint("coral", __name__)

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(ROOT, "models", "coral_resnet50_ft")

MODEL_PATH = os.path.join(MODEL_DIR, "model.keras")
CLASSES_PATH = os.path.join(MODEL_DIR, "classes.json")

# Load classes
with open(CLASSES_PATH, "r") as f:
    classes = json.load(f)

# Load model
model = tf.keras.models.load_model(MODEL_PATH)
H, W = model.input_shape[1], model.input_shape[2]

def preprocess(image: Image.Image):
    image = image.convert("RGB").resize((W, H))
    x = np.asarray(image, dtype=np.float32)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return np.expand_dims(x, 0)

@coral_bp.route("/predict", methods=["POST"])
def predict_coral():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_bytes = file.read()

    try:
        img = Image.open(io.BytesIO(img_bytes))
    except Exception:
        return jsonify({"error": "Invalid image"}), 400

    x = preprocess(img)
    preds = model(x, training=False)
    probs = tf.nn.softmax(preds, axis=-1).numpy()[0]

    idx = int(np.argmax(probs))
    label = classes[idx]

    return jsonify({
        "label": label,
        "probabilities": {
            classes[i]: float(probs[i]) for i in range(len(classes))
        }
    })
