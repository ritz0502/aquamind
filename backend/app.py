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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
