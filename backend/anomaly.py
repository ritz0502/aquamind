# backend/anomaly.py

from flask import Blueprint, request, jsonify
import random
import os
import sys

# --- Add model path dynamically ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models", "anomaly_detection", "sst_anomaly", "src")

# Add ML model folder to python path
sys.path.insert(0, MODEL_DIR)

# If you have any python model file inside /src, import here
# Example: from your_model import YourModelClass
# If not needed, ignore – your current anomaly logic uses random values anyway


anomaly_bp = Blueprint("anomaly", __name__)


def generate_anomaly_chart():
    return [
        {'time': f'{i}:00', 'reading': random.randint(50, 95)}
        for i in range(1, 13)
    ]


@anomaly_bp.route("/run", methods=["POST"])
def anomaly_detection():
    try:
        data = request.json

        temperature = float(data.get('temperature', 25))
        salinity = float(data.get('salinity', 35))
        pH = float(data.get('pH', 8.1))

        anomalies = []
        risk_level = "Low Risk"

        if abs(temperature - 25) > 3:
            anomalies.append(
                f"Temperature anomaly detected: {temperature}°C (expected ~25°C)"
            )
            risk_level = "Medium Risk"

        if abs(salinity - 35) > 3:
            anomalies.append(
                f"Salinity anomaly detected: {salinity} PSU (expected ~35 PSU)"
            )
            risk_level = "Medium Risk"

        if abs(pH - 8.1) > 0.3:
            anomalies.append(
                f"pH anomaly detected: {pH} (expected ~8.1)"
            )
            risk_level = "High Risk"

        if not anomalies:
            anomalies.append("No significant anomalies detected. Parameters within normal ranges.")
            insight = "All ocean parameters are within expected ranges. Ecosystem appears stable."
        else:
            insight = f"{len(anomalies)} anomaly detected. Investigate potential environmental changes."

        return jsonify({
            'status': 'success',
            'model': 'anomalies',
            'results': {
                'risk_level': risk_level,
                'anomalies': anomalies,
                'insight': insight,
                'chartData': generate_anomaly_chart()
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
