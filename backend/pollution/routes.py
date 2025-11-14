from flask import request, jsonify
from . import pollution
import os

# Import model inference
from models.marine_pollution.scripts.infer_combined import predict



@pollution.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "🛑 Marine Pollution Detection API",
        "status": "running",
        "endpoints": {
            "POST /infer": "Upload an image and get pollution prediction"
        }
    })


@pollution.route("/infer", methods=["POST"])
def infer_pollution():
    try:
        # No file uploaded
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded"
            }), 400

        file = request.files["file"]

        # Run model inference
        result = predict(file)

        return jsonify({
            "status": "success",
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }), 500
