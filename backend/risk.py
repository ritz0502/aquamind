# risk.py
from flask import Blueprint, request, jsonify, send_file
import subprocess
import os
from datetime import datetime
import traceback
import sys

# NEW IMPORTS FOR MEHI + STORAGE
from backend.utils.storage import load, save
from backend.utils.mehi import calculate_mehi

risk = Blueprint("risk", __name__)

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "..", "models", "risk_prediction", "src")
DATA_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "models", "risk_prediction", "data")
)

# Ensure necessary directories exist
os.makedirs(os.path.join(DATA_DIR, "reports"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "risk"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "plots"), exist_ok=True)


@risk.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "🌊 Marine Risk Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /run_pipeline": "Run the risk prediction pipeline",
            "GET /get_plot": "Fetch risk plot image",
            "GET /health": "Check API health"
        }
    })


@risk.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "data_dir": DATA_DIR,
        "src_dir": SRC_DIR
    })


@risk.route("/run_pipeline", methods=["POST", "OPTIONS"])
def run_pipeline():

    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        try:
            lat = float(data.get("lat"))
            lon = float(data.get("lon"))
        except:
            return jsonify({"status": "error", "message": "Invalid lat/lon"}), 400

        if not (-90 <= lat <= 90):
            return jsonify({"status": "error", "message": "Invalid latitude"}), 400

        if not (-180 <= lon <= 180):
            return jsonify({"status": "error", "message": "Invalid longitude"}), 400

        forecast_days = int(data.get("forecast_days", 30))
        quick_mode = data.get("quick_mode", True)

        cmd = [
            sys.executable, os.path.join(SRC_DIR, "run_pipeline.py"),
            "--lat", str(lat),
            "--lon", str(lon),
            "--forecast_days", str(forecast_days)
        ]

        if quick_mode:
            cmd.append("--quick_mode")

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=300
        )

        report_path = os.path.join(DATA_DIR, "reports", f"marine_risk_report_{lat}_{lon}.txt")
        plot_path = os.path.join(DATA_DIR, "plots", f"marine_risk_index_{lat}_{lon}.png")

        if not os.path.exists(report_path):
            return jsonify({
                "status": "success",
                "message": "Pipeline completed (no report generated)",
                "coordinates": {"lat": lat, "lon": lon}
            }), 200

        # -------------------------------
        # READ REPORT AND EXTRACT RISK
        # -------------------------------
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()

        risk_level = "Unknown"
        for line in report_text.splitlines():
            if "Risk Level:" in line:
                risk_level = line.split(":")[-1].strip().capitalize()
                break

        # -------------------------------
        # SAVE TO combined_outputs.json
        # -------------------------------
        combined = load()

        combined["risk"] = {
            "risk_level": risk_level,
            "coordinates": {"lat": lat, "lon": lon},
            "report_path": report_path,
            "plot_path": plot_path
        }

        # ensure pollution exists
        if "pollution" not in combined:
            combined["pollution"] = {}

        # ensure coral exists (dummy)
        if "coral" not in combined:
            combined["coral"] = {"health_score": 0.7}

        # calculate MEHI
        combined["mehi"] = calculate_mehi(combined)

        save(combined)
        # --------------------------------

        return jsonify({
            "status": "success",
            "risk_level": risk_level,
            "mehi": combined["mehi"],
            "coordinates": {"lat": lat, "lon": lon}
        }), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }), 500


@risk.route("/get_plot", methods=["GET"])
def get_plot():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        possible_names = [
            f"marine_risk_index_{lat}_{lon}.png",
            f"marine_risk_index_{float(lat):.1f}_{float(lon):.1f}.png",
            f"marine_risk_index_{float(lat)}_{float(lon)}.png"
        ]

        for name in possible_names:
            path = os.path.join(DATA_DIR, "plots", name)
            if os.path.exists(path):
                return send_file(path, mimetype="image/png")

        return jsonify({"status": "error", "message": "Plot not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@risk.route("/get_risk_data", methods=["GET"])
def get_risk_data():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        csv_path = os.path.join(DATA_DIR, "risk", f"marine_risk_forecast_{lat}_{lon}.csv")

        if not os.path.exists(csv_path):
            return jsonify({"status": "error", "message": "CSV not found"}), 404

        import pandas as pd
        df = pd.read_csv(csv_path)

        return jsonify({"status": "success", "data": df.to_dict(orient="records")})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@risk.route("/get_report", methods=["GET"])
def get_report():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        possible_names = [
            f"marine_risk_report_{lat}_{lon}.txt",
            f"marine_risk_report_{float(lat):.1f}_{float(lon):.1f}.txt",
            f"marine_risk_report_{float(lat)}_{float(lon)}.txt",
        ]

        for name in possible_names:
            path = os.path.join(DATA_DIR, "reports", name)
            if os.path.exists(path):
                return send_file(path, mimetype="text/plain")

        return jsonify({"status": "error", "message": "Report not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
