import os
import json

# Always compute absolute path regardless of where app runs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Full absolute path
FILE_PATH = os.path.join(DATA_DIR, "combined_outputs.json")

# Create folder if missing
os.makedirs(DATA_DIR, exist_ok=True)

def load():
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure folder
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
