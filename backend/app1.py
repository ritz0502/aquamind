# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
from datetime import datetime
import traceback

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure necessary directories exist
os.makedirs(os.path.join(DATA_DIR, "reports"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "risk"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "plots"), exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    """API information endpoint."""
    return jsonify({
        "message": "🌊 Marine Risk Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /run_pipeline": {
                "description": "Run full pipeline for given coordinates",
                "parameters": {
                    "lat": "Latitude (-90 to 90)",
                    "lon": "Longitude (-180 to 180)",
                    "forecast_days": "Number of forecast days (default: 30)",
                    "quick_mode": "Enable quick processing mode (default: true)"
                }
            },
            "GET /get_plot": {
                "description": "Fetch risk plot image",
                "parameters": {
                    "lat": "Latitude",
                    "lon": "Longitude"
                }
            },
            "GET /health": {
                "description": "Check API health status"
            }
        }
    })


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "data_dir": DATA_DIR,
        "src_dir": SRC_DIR
    })


@app.route("/run_pipeline", methods=["POST", "OPTIONS"])
def run_pipeline():
    """Run the marine risk prediction pipeline for given coordinates."""
    
    # Handle preflight request
    if request.method == "OPTIONS":
        return "", 204
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided in request body"
            }), 400
        
        # Extract and validate parameters
        try:
            lat = float(data.get("lat"))
            lon = float(data.get("lon"))
        except (TypeError, ValueError):
            return jsonify({
                "status": "error",
                "message": "Invalid latitude or longitude. Must be numeric values."
            }), 400
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90):
            return jsonify({
                "status": "error",
                "message": "Latitude must be between -90 and 90"
            }), 400
        
        if not (-180 <= lon <= 180):
            return jsonify({
                "status": "error",
                "message": "Longitude must be between -180 and 180"
            }), 400
        
        forecast_days = int(data.get("forecast_days", 30))
        quick_mode = data.get("quick_mode", True)
        
        # Validate forecast_days
        if not (1 <= forecast_days <= 365):
            return jsonify({
                "status": "error",
                "message": "Forecast days must be between 1 and 365"
            }), 400
        
        print(f"🌊 Running pipeline for ({lat}, {lon}) | {forecast_days} days | quick={quick_mode}")
        
        # Construct command
        cmd = [
            "python", os.path.join(SRC_DIR, "run_pipeline.py"),
            "--lat", str(lat),
            "--lon", str(lon),
            "--forecast_days", str(forecast_days)
        ]
        
        if quick_mode:
            cmd.append("--quick_mode")
        
        # Run the pipeline
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print("Pipeline stdout:", result.stdout)
        if result.stderr:
            print("Pipeline stderr:", result.stderr)
        
        # Locate generated files
        report_path = os.path.join(DATA_DIR, "reports", f"marine_risk_report_{lat}_{lon}.txt")
        risk_csv = os.path.join(DATA_DIR, "risk", f"marine_risk_forecast_{lat}_{lon}.csv")
        plot_path = os.path.join(DATA_DIR, "plots", f"marine_risk_index_{lat}_{lon}.png")
        
        # Check if report file exists
        if not os.path.exists(report_path):
            return jsonify({
                "status": "error",
                "message": f"Report file not generated. Pipeline may have failed silently.",
                "expected_path": report_path
            }), 500
        
        # Read report text
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()
        
        # Extract risk level from report
        risk_level = "Unknown"
        for line in report_text.splitlines():
            if "Risk Level:" in line:
                risk_level = line.split(":")[-1].strip().capitalize()
                break
        
        # Check if other files exist
        files_status = {
            "report": os.path.exists(report_path),
            "risk_csv": os.path.exists(risk_csv),
            "plot": os.path.exists(plot_path)
        }
        
        return jsonify({
            "status": "success",
            "message": "Pipeline executed successfully",
            "coordinates": {
                "lat": lat,
                "lon": lon
            },
            "risk_level": risk_level,
            "report_text": report_text,
            "files": files_status,
            "paths": {
                "report": report_path,
                "risk_data": risk_csv,
                "plot": plot_path
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "error",
            "message": "Pipeline execution timed out. Try using quick_mode or reducing forecast_days."
        }), 504
        
    except subprocess.CalledProcessError as e:
        error_details = {
            "stdout": e.stdout if hasattr(e, 'stdout') else None,
            "stderr": e.stderr if hasattr(e, 'stderr') else None,
            "returncode": e.returncode
        }
        print(f"Pipeline failed with error: {error_details}")
        
        return jsonify({
            "status": "error",
            "message": f"Pipeline execution failed with return code {e.returncode}",
            "details": error_details
        }), 500
        
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": f"Required file not found: {str(e)}",
            "suggestion": "Ensure run_pipeline.py exists in the src directory"
        }), 500
        
    except Exception as e:
        print(f"Unexpected error: {traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }), 500


@app.route("/get_plot", methods=["GET"])
def get_plot():
    """Serve the latest risk plot as an image."""
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        
        if not lat or not lon:
            return jsonify({
                "status": "error",
                "message": "Missing lat or lon parameter"
            }), 400
        
        plot_path = os.path.join(DATA_DIR, "plots", f"marine_risk_index_{lat}_{lon}.png")
        
        if os.path.exists(plot_path):
            return send_file(
                plot_path,
                mimetype="image/png",
                as_attachment=False,
                download_name=f"marine_risk_plot_{lat}_{lon}.png"
            )
        else:
            return jsonify({
                "status": "error",
                "message": "Plot not found",
                "expected_path": plot_path
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error serving plot: {str(e)}"
        }), 500


@app.route("/get_risk_data", methods=["GET"])
def get_risk_data():
    """Serve the risk data CSV as JSON."""
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        
        if not lat or not lon:
            return jsonify({
                "status": "error",
                "message": "Missing lat or lon parameter"
            }), 400
        
        csv_path = os.path.join(DATA_DIR, "risk", f"marine_risk_forecast_{lat}_{lon}.csv")
        
        if os.path.exists(csv_path):
            import pandas as pd
            df = pd.read_csv(csv_path)
            return jsonify({
                "status": "success",
                "data": df.to_dict(orient="records")
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Risk data CSV not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error serving risk data: {str(e)}"
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": ["/", "/run_pipeline", "/get_plot", "/get_risk_data", "/health"]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "details": str(e)
    }), 500


if __name__ == "__main__":
    print("🌊 Marine Risk Prediction API Starting...")
    print(f"📁 Data Directory: {DATA_DIR}")
    print(f"📁 Source Directory: {SRC_DIR}")
    print("🔗 Server running on http://localhost:5000")
    print("✅ CORS enabled for http://localhost:3000 and http://localhost:5173")
    
    app.run(host="0.0.0.0", port=5000, debug=True)