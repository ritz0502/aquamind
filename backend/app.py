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

app = Flask(__name__)
CORS(app)

# ------- LOAD ONLY WORKING MODELS -------

# ANOMALY DETECTION
from anomaly import anomaly_bp
app.register_blueprint(anomaly_bp, url_prefix="/api/anomalies")

# CORAL HEALTH MODEL
from coral import coral_bp
app.register_blueprint(coral_bp, url_prefix="/coral")

# -------- COMMENTED OUT OLD MODELS --------
# """
# from risk import risk
# from pollution.routes import pollution

# app.register_blueprint(risk, url_prefix="/risk")
# app.register_blueprint(pollution, url_prefix="/pollution")
# """

# -------- ROOT ENDPOINT --------
@app.route("/")
def home():
    return {"message": "Backend running (anomaly + coral models active)"}

# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
