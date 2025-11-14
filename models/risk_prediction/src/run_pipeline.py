# # src/run_pipeline.py
# import subprocess
# import argparse
# import os
# import time
# import sys
# from datetime import datetime

# BASE_DIR = os.path.dirname(__file__)

# # Pipeline stages in order (label, script)
# STAGES = [
#     ("📥 Data Fetching", "fetch_data.py"),
#     ("🧹 Preprocessing", "preprocess.py"),
#     ("🔮 Prophet Forecast", "train_prophet.py"),
#     ("🧠 LSTM Forecast", "train_lstm.py"),
#     ("⚙️ Fusion & Risk", "forecast_and_risk.py"),
#     ("🗒️ Report Generation", "llm_report.py")
# ]

# def run_stage(label, script, lat, lon, forecast_days, history_days):
#     print(f"\n==============================")
#     print(f"{label} ({script})")
#     print("==============================")

#     script_path = os.path.join(BASE_DIR, script)
#     if not os.path.exists(script_path):
#         print(f"❌ Script not found: {script_path}")
#         return False

#     # Use the same Python interpreter that's running this script (ensures venv)
#     cmd = [sys.executable, script_path, "--lat", str(lat), "--lon", str(lon)]

#     # Only pass extra args to scripts that expect them
#     script_name = os.path.basename(script)
#     if script_name == "fetch_data.py":
#         # fetch_data expects --days (historical window)
#         cmd += ["--days", str(history_days)]
#     if script_name in ("train_prophet.py", "train_lstm.py"):
#         # these accept --forecast_days
#         cmd += ["--forecast_days", str(forecast_days)]
#     # forecast_and_risk.py and llm_report.py do not need forecast_days

#     # Run the script
#     start = time.time()
#     try:
#         subprocess.run(cmd, check=True)
#         duration = time.time() - start
#         print(f"✅ {label} completed in {duration:.1f}s.")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Error in {label}: {e}")
#         return False
#     except Exception as e:
#         print(f"❌ Unexpected error in {label}: {e}")
#         return False


# def main(lat, lon, forecast_days, history_days):
#     print("\n==============================")
#     print("🌊 MARINE RISK PREDICTION PIPELINE")
#     print("==============================")
#     print(f"Coordinates: ({lat}, {lon})")
#     print(f"Forecast horizon: {forecast_days} days | History window: {history_days} days")
#     print("==============================\n")

#     pipeline_start = time.time()

#     for label, script in STAGES:
#         success = run_stage(label, script, lat, lon, forecast_days, history_days)
#         if not success:
#             print(f"⚠️ Pipeline stopped at stage: {label}")
#             return

#     total_time = (time.time() - pipeline_start) / 60
#     print("\n==============================")
#     print("✅ PIPELINE COMPLETED SUCCESSFULLY")
#     print("==============================")
#     print(f"🕒 Total time taken: {total_time:.2f} minutes")
#     print(f"📊 Reports saved in: data/reports/")
#     print(f"🖼️ Plots saved in: data/plots/")
#     print(f"💾 Forecast data saved in: data/forecasts/")
#     print(f"\nReport generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
#     print("==============================\n")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run full marine risk prediction pipeline.")
#     parser.add_argument("--lat", type=float, required=True, help="Latitude coordinate")
#     parser.add_argument("--lon", type=float, required=True, help="Longitude coordinate")
#     parser.add_argument("--forecast_days", type=int, default=30, help="Forecast horizon in days (passed to train scripts)")
#     parser.add_argument("--history_days", type=int, default=60, help="Historical days to fetch (passed to fetch_data.py as --days)")
#     args = parser.parse_args()

#     main(args.lat, args.lon, args.forecast_days, args.history_days)











# src/run_pipeline.py
import subprocess
import argparse
import os
import time
import sys
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')


BASE_DIR = os.path.dirname(__file__)

# --- CONFIGURABLE PIPELINE STAGES ---
STAGES = [
    ("📥 Data Fetching", "fetch_data.py"),
    ("🧹 Preprocessing", "preprocess.py"),
    ("🔮 Prophet Forecast", "train_prophet.py"),
    ("🧠 LSTM Forecast", "train_lstm.py"),
    ("⚙️ Fusion & Risk", "forecast_and_risk.py"),
    ("🗒️ Report Generation", "llm_report.py")
]

# --- FILE PATH HELPERS ---
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
MODEL_DIR = os.path.join(DATA_DIR, "models")
REPORT_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(MODEL_DIR, exist_ok=True)


def run_stage(label, script, lat, lon, forecast_days, history_days, quick_mode):
    """Runs one pipeline stage intelligently, skipping or caching if possible."""
    print(f"\n==============================")
    print(f"{label} ({script})")
    print("==============================")

    script_path = os.path.join(BASE_DIR, script)
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False

    # 1️⃣ Determine if we can skip
    can_skip = False
    script_name = os.path.basename(script)

    if script_name == "fetch_data.py":
        # Skip if raw data already exists and is recent
        cached_files = [f for f in os.listdir(RAW_DIR) if str(lat) in f and str(lon) in f]
        if cached_files and quick_mode:
            print(f"⚡ Using cached marine data ({len(cached_files)} files).")
            return True

    elif script_name == "train_prophet.py":
        # Skip if prophet forecasts exist
        cached_forecasts = [f for f in os.listdir(FORECAST_DIR)
                            if "forecast_prophet" in f and str(lat) in f and str(lon) in f]
        if cached_forecasts and quick_mode:
            print(f"⚡ Using cached Prophet forecasts ({len(cached_forecasts)} files).")
            return True

    elif script_name == "train_lstm.py":
        cached_forecasts = [f for f in os.listdir(FORECAST_DIR)
                            if "lstm_forecast" in f and str(lat) in f and str(lon) in f]
        if cached_forecasts and quick_mode:
            print(f"⚡ Using cached LSTM forecasts ({len(cached_forecasts)} files).")
            return True

    elif script_name == "forecast_and_risk.py":
        risk_file = os.path.join(DATA_DIR, "risk", f"marine_risk_forecast_{lat}_{lon}.csv")
        if os.path.exists(risk_file) and quick_mode:
            print(f"⚡ Using cached risk fusion results.")
            return True

    elif script_name == "llm_report.py":
        report_file = os.path.join(REPORT_DIR, f"marine_risk_report_{lat}_{lon}.txt")
        if os.path.exists(report_file) and quick_mode:
            print(f"⚡ Report already exists — skipping generation.")
            return True

    # 2️⃣ Run the script
    cmd = [sys.executable, script_path, "--lat", str(lat), "--lon", str(lon)]

    # Only pass certain args to relevant scripts
    if script_name == "fetch_data.py":
        cmd += ["--days", str(history_days)]
    elif script_name in ("train_prophet.py", "train_lstm.py"):
        cmd += ["--forecast_days", str(forecast_days)]
        if quick_mode and script_name == "train_prophet.py":
            cmd += ["--fast_mode"]

    start = time.time()
    try:
        subprocess.run(cmd, check=True)
        duration = time.time() - start
        print(f"✅ {label} completed in {duration:.1f}s.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {label}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {label}: {e}")
        return False


def main(lat, lon, forecast_days, history_days, quick_mode):
    print("\n==============================")
    print("🌊 SMART-CACHED MARINE RISK PIPELINE")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print(f"Forecast horizon: {forecast_days} days | History window: {history_days} days")
    print(f"Mode: {'⚡ QUICK' if quick_mode else '🧠 FULL TRAIN'}")
    print("==============================\n")

    pipeline_start = time.time()

    for label, script in STAGES:
        success = run_stage(label, script, lat, lon, forecast_days, history_days, quick_mode)
        if not success:
            print(f"⚠️ Pipeline stopped at stage: {label}")
            return

    total_time = (time.time() - pipeline_start) / 60
    print("\n==============================")
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("==============================")
    print(f"🕒 Total time taken: {total_time:.2f} minutes")
    print(f"📊 Reports saved in: data/reports/")
    print(f"🖼️ Plots saved in: data/plots/")
    print(f"💾 Forecast data saved in: data/forecasts/")
    print(f"\nReport generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("==============================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run optimized marine risk prediction pipeline.")
    parser.add_argument("--lat", type=float, required=True, help="Latitude coordinate")
    parser.add_argument("--lon", type=float, required=True, help="Longitude coordinate")
    parser.add_argument("--forecast_days", type=int, default=30, help="Forecast horizon in days")
    parser.add_argument("--history_days", type=int, default=60, help="Days of historical data to fetch")
    parser.add_argument("--quick_mode", action="store_true", help="Enable caching and fast Prophet/LSTM mode")
    args = parser.parse_args()

    main(args.lat, args.lon, args.forecast_days, args.history_days, args.quick_mode)
