# backend/human_activity.py

from flask import Blueprint, request, jsonify
import subprocess
import os
import sys
import re

human_activity_bp = Blueprint("human_activity_bp", __name__)

@human_activity_bp.route("/run", methods=["POST"])
def run_human_activity():
    """
    Run human_activity_risk/main.py for inference.
    """
    try:
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")

        if lat is None or lon is None:
            return jsonify({"error": "Missing latitude or longitude"}), 400

        # Model directory
        BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        MODEL_DIR = os.path.join(BASE, "models", "human_activity_risk")
        os.chdir(MODEL_DIR)

        # Use active venv python
        cmd = [sys.executable, "main.py", "--lat", str(lat), "--lon", str(lon)]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        stdout, stderr = process.stdout, process.stderr

        print("\n---- STDOUT ----\n", stdout)
        print("\n---- STDERR ----\n", stderr)

        if process.returncode != 0:
            return jsonify({
                "error": "Model failed",
                "stderr": stderr
            }), 500

        def find(pattern):
            m = re.search(pattern, stdout)
            return m.group(1).strip() if m else None

        result = {
            "score": float(find(r"activity_risk\s*→\s*([\d.]+)") or 0),
            "badge": find(r"risk badge\s*→\s*(.+)") or "N/A",
            "features": {
                "ports": int(find(r"ports:\s*(\d+)") or 0),
                "industries": int(find(r"industries:\s*(\d+)") or 0),
                "ships": int(find(r"ships:\s*(\d+)") or 0),
                "hotels": int(find(r"hotels:\s*(\d+)") or 0),
            },
            "recommendation": find(r"recommendation\s*→\s*(.*)") or "No recommendation"
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
