# src/run_pipeline.py

import subprocess
import argparse
import os
import time
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(__file__)

# ============================
# Pipeline Stages
# ============================
STAGES = [
    ("📥 Data Fetching", "fetch_data.py"),
    ("🧹 Preprocessing", "preprocess.py"),
    ("🔮 Prophet Forecast", "train_prophet.py"),
    ("🧠 LSTM Forecast", "train_lstm.py"),
    ("⚙️ Fusion & Risk", "forecast_and_risk.py"),
    ("🗒️ Report Generation", "llm_report.py")
]

# ============================
# Data Directories
# ============================
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
REPORT_DIR = os.path.join(DATA_DIR, "reports")
RISK_DIR = os.path.join(DATA_DIR, "risk")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FORECAST_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(RISK_DIR, exist_ok=True)

# ============================
# Run a single stage
# ============================
def run_stage(label, script, lat, lon, forecast_days, history_days, quick_mode):
    print("\n==============================")
    print(f"{label} ({script})")
    print("==============================")

    script_path = os.path.join(BASE_DIR, script)

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False

    script_name = os.path.basename(script)

    # ======================================
    # QUICK MODE (SKIP IF CACHE EXISTS)
    # ======================================
    if quick_mode:
        if script_name == "fetch_data.py":
            cached = [f for f in os.listdir(RAW_DIR) if f"{lat}_{lon}" in f]
            if cached:
                print(f"⚡ Cached RAW data found → skipping fetch")
                return True

        if script_name == "train_prophet.py":
            cached = [f for f in os.listdir(FORECAST_DIR)
                      if "forecast_prophet" in f and f"{lat}_{lon}" in f]
            if cached:
                print("⚡ Cached Prophet forecast found → skipping")
                return True

        if script_name == "train_lstm.py":
            cached = [f for f in os.listdir(FORECAST_DIR)
                      if "forecast_lstm" in f and f"{lat}_{lon}" in f]
            if cached:
                print("⚡ Cached LSTM forecast found → skipping")
                return True

        if script_name == "forecast_and_risk.py":
            risk_file = os.path.join(RISK_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
            if os.path.exists(risk_file):
                print("⚡ Cached risk fusion output found → skipping")
                return True

        if script_name == "llm_report.py":
            report_file = os.path.join(REPORT_DIR, f"marine_risk_report_{lat}_{lon}.txt")
            if os.path.exists(report_file):
                print("⚡ Report already exists → skipping")
                return True

    # ======================================
    # BUILD COMMAND
    # ======================================
    cmd = [sys.executable, script_path, "--lat", str(lat), "--lon", str(lon)]

    if script_name == "fetch_data.py":
        cmd += ["--days", str(history_days)]

    if script_name in ("train_prophet.py", "train_lstm.py"):
        cmd += ["--forecast_days", str(forecast_days)]
        if quick_mode and script_name == "train_prophet.py":
            cmd += ["--fast_mode"]

    # ======================================
    # EXECUTE
    # ======================================
    try:
        start = time.time()
        subprocess.run(cmd, check=True)
        print(f"✅ {label} completed in {time.time() - start:.1f}s")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error in stage {label}: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error in stage {label}: {e}")
        return False


# ============================
# MAIN PIPELINE
# ============================
def main(lat, lon, forecast_days, history_days, quick_mode):
    print("\n==============================")
    print("🌊 SMART-CACHED MARINE RISK PIPELINE")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print(f"Forecast horizon: {forecast_days} days")
    print(f"History window: {history_days} days")
    print(f"Mode: {'⚡ QUICK' if quick_mode else '🧠 FULL TRAIN'}")
    print("==============================\n")

    pipeline_start = time.time()

    for label, script in STAGES:
        ok = run_stage(label, script, lat, lon, forecast_days, history_days, quick_mode)
        if not ok:
            print(f"⚠️ Pipeline stopped at: {label}")
            return

    print("\n==============================")
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("==============================")
    print(f"🕒 Total time: {(time.time() - pipeline_start)/60:.2f} minutes")
    print(f"📊 Reports saved in data/reports/")
    print(f"🖼️ Plots saved in data/plots/")
    print(f"💾 Forecast data saved in data/forecasts/")
    print(f"Report generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("==============================\n")


# ============================
# CLI ENTRY
# ============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Marine Risk Prediction Pipeline")
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--forecast_days", type=int, default=30)
    parser.add_argument("--history_days", type=int, default=60)
    parser.add_argument("--quick_mode", action="store_true")
    args = parser.parse_args()

    main(args.lat, args.lon, args.forecast_days, args.history_days, args.quick_mode)
