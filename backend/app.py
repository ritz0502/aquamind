import sys
import os

# ==========================================
#  PATH CONFIGURATION
# ==========================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")

print("ROOT_DIR =", ROOT_DIR)
print("MODELS_DIR =", MODELS_DIR)

# Add to Python path
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, MODELS_DIR)

# ==========================================
#  FLASK APP SETUP
# ==========================================
from flask import Flask, jsonify
from flask_cors import CORS

# storage loader
try:
    from backend.utils.storage import load
except:
    # fallback if backend folder is not used
    from utils.storage import load

app = Flask(__name__, static_folder="static")
CORS(app)

# ==========================================
#  REGISTER ALL MODEL ROUTES
# ==========================================

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


# ==========================================
#  ROOT ENDPOINT
# ==========================================
@app.route("/")
def home():
    return {
        "message": "Backend running",
        "models": ["anomaly", "coral", "risk", "pollution", "activity"]
    }

# ==========================================
#  SUMMARY ENDPOINT
# ==========================================
@app.route("/summary", methods=["GET"])
def summary():

    data = load()

    # ensure coral exists
    data.setdefault("coral", {"health_score": 0.7})

    # ensure risk exists
    data.setdefault("risk", {"risk_level": "Unknown"})

    # ensure pollution exists
    data.setdefault("pollution", {})

    # ensure human activity exists
    data.setdefault("activity", {"impact_score": "Unknown"})

    return jsonify(data)


# ==========================================
#  RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
