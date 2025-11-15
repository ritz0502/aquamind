import sys
import os


from flask import send_from_directory

# ------- PATH CONFIG ---------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")

print("ROOT_DIR =", ROOT_DIR)
print("MODELS_DIR =", MODELS_DIR)

# Add project root + models folder to Python path
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, MODELS_DIR)

# ------- FLASK SETUP --------
from flask import Flask, jsonify
from flask_cors import CORS

# NEW: storage import
from backend.utils.storage import load

app = Flask(__name__, static_folder="static")
CORS(app)

# =======================================
#  REGISTER ALL AVAILABLE MODEL ROUTES
# =======================================

# -------- ANOMALY DETECTION --------
try:
    from anomaly import anomaly_bp
    app.register_blueprint(anomaly_bp, url_prefix="/api/anomalies")
    print("✓ Anomaly model loaded")
except Exception as e:
    print("✗ Failed to load anomaly model:", e)

# -------- CORAL HEALTH MODEL --------
try:
    from coral import coral_bp
    app.register_blueprint(coral_bp, url_prefix="/coral")
    print("✓ Coral model loaded")
except Exception as e:
    print("✗ Failed to load coral model:", e)

# -------- RISK MODEL --------
try:
    from risk import risk
    app.register_blueprint(risk, url_prefix="/risk")
    print("✓ Risk model loaded")
except Exception as e:
    print("✗ Failed to load risk model:", e)

# -------- POLLUTION MODEL --------
try:
    from pollution.routes import pollution
    app.register_blueprint(pollution, url_prefix="/pollution")
    print("✓ Pollution model loaded")
except Exception as e:
    print("✗ Failed to load pollution model:", e)

# -------- HUMAN ACTIVITY MODEL --------
try:
    from human_activity import human_activity_bp
    app.register_blueprint(human_activity_bp, url_prefix="/activity")
    print("✓ Human Activity model loaded")
except Exception as e:
    print("✗ Failed to load Human Activity model:", e)


# -------- ROOT ENDPOINT --------
@app.route("/")
def home():
    return {
        "message": "Backend running",
        "models": ["anomaly", "coral", "risk", "pollution", "activity"]
    }


# -------- NEW: SUMMARY ENDPOINT --------
@app.route("/summary", methods=["GET"])
def summary():
    """
    Returns combined outputs of all models:
    - risk
    - pollution
    - coral
    - mehi
    """
    data = load()

    # ensure coral exists
    if "coral" not in data:
        data["coral"] = {"health_score": 0.7}

    # ensure risk exists
    if "risk" not in data:
        data["risk"] = {"risk_level": "Unknown"}

    # ensure pollution exists
    if "pollution" not in data:
        data["pollution"] = {}

    # ensure human activity exists
    if "activity" not in data:
        data["activity"] = {"impact_score": "Unknown"}

    return jsonify(data)


@app.route("/heatmaps/<path:filename>")
def serve_heatmap(filename):
    heatmap_folder = os.path.join(os.path.dirname(__file__), "heatmaps")
    return send_from_directory(heatmap_folder, filename)



# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
