import json
import os

# Path to combined JSON file
FILE_PATH = os.path.join("backend", "data", "combined_outputs.json")

# Ensure directory exists
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

# If file does not exist, create it with empty structure
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump({}, f, indent=4)


def load():
    """Load combined model outputs."""
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return {}   # fallback safe


def save(data: dict):
    """Save combined model outputs."""
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
