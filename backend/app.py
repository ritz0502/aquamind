<<<<<<< HEAD
import sys, os
from flask import Flask
from flask_cors import CORS

# absolute path to aquamind root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")

# Add /aquamind and /aquamind/models to Python path
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, MODELS_DIR)

from risk import risk
from pollution.routes import pollution

# ------------------------------
# IMPORTANT: only ONE app instance
# WITH static folder enabled
# ------------------------------
app = Flask(__name__, static_folder="static")

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(risk, url_prefix="/risk")
app.register_blueprint(pollution, url_prefix="/pollution")

@app.route("/")
def home():
    return {"message": "Master API running"}

=======
import sys
import os

# ------- PATH CONFIG ---------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")

print("ROOT_DIR =", ROOT_DIR)
print("MODELS_DIR =", MODELS_DIR)

# Add project root + models folder to Python path
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, MODELS_DIR)

# ------- FLASK SETUP --------
from flask import Flask
from flask_cors import CORS

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

# -------- ROOT ENDPOINT --------
@app.route("/")
def home():
    return {
        "message": "Backend running",
        "models": ["anomaly", "coral", "risk", "pollution"]
    }

# -------- RUN SERVER --------
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
