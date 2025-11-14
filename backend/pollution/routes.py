from flask import request, jsonify
from . import pollution
import os

# Import model inference
from models.marine_pollution.scripts.infer_combined import predict

# NEW: Import JSON storage + MEHI calculator
from backend.utils.storage import load, save
from backend.utils.mehi import calculate_mehi


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

        # Fix paths to annotated + mask
        annotated_path = result.get("annotated")
        mask_path = result.get("mask")

        # Convert absolute Windows paths → relative URLs inside /static
        if annotated_path:
            result["annotated"] = "static/" + os.path.basename(annotated_path)

        if mask_path:
            result["mask"] = "static/" + os.path.basename(mask_path)

        # ----------------------------------------------------------
        # 🔵 NEW: Store pollution output + update MEHI JSON
        # ----------------------------------------------------------
        data = load()  # load existing combined outputs

        data["pollution"] = result  # save pollution result

        # ensure coral exists (dummy placeholder for now)
        if "coral" not in data:
            data["coral"] = {"health_score": 0.7}

        # ensure risk exists
        if "risk" not in data:
            data["risk"] = {"risk_level": "Medium"}

        # calculate MEHI
        data["mehi"] = calculate_mehi(data)

        # save everything back
        save(data)
        # ----------------------------------------------------------

        return jsonify({
            "status": "success",
            "prediction": result,
            "mehi": data["mehi"]    # return MEHI in API response
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }), 500
