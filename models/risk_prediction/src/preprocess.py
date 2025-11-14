import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ======================================
# PATHS
# ======================================
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


# ======================================
# HELPERS
# ======================================
def load_and_clean_csv(file_path, variable_name):
    """Load raw CSV, clean it, and return standardized format."""

    if not os.path.exists(file_path):
        print(f"⚠️ File missing: {file_path}")
        return pd.DataFrame(columns=["time", variable_name])

    try:
        df = pd.read_csv(file_path)

        if "time" not in df.columns:
            raise ValueError("Missing 'time' column")

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])

        # Find correct variable
        if variable_name not in df.columns:
            matches = [c for c in df.columns if variable_name.lower() in c.lower()]
            if matches:
                df.rename(columns={matches[0]: variable_name}, inplace=True)
            else:
                print(f"⚠️ Variable '{variable_name}' not found in {file_path}")
                df[variable_name] = np.nan

        df = df[["time", variable_name]]
        df = df.drop_duplicates(subset=["time"]).sort_values("time")
        df[variable_name] = pd.to_numeric(df[variable_name], errors="coerce")
        df[variable_name] = df[variable_name].interpolate(limit_direction="both")

        return df

    except Exception as e:
        print(f"❌ Failed to load {file_path}: {e}")
        return pd.DataFrame(columns=["time", variable_name])


# ======================================
# MAIN PREPROCESSING FUNCTION
# ======================================
def preprocess_data(lat, lon):

    print("\n==============================")
    print("🌊 MARINE DATA PREPROCESSOR")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print("==============================")

    # --- RAW FILES ---
    sst_path = os.path.join(RAW_DIR, f"open_meteo_{lat}_{lon}.csv")
    sal_path = os.path.join(RAW_DIR, f"salinity_{lat}_{lon}.csv")
    chl_path = os.path.join(RAW_DIR, f"chlor_a_{lat}_{lon}.csv")

    # load
    sst = load_and_clean_csv(sst_path, "sea_surface_temperature_max")
    sal = load_and_clean_csv(sal_path, "salinity")
    chl = load_and_clean_csv(chl_path, "chlor_a")

    # merge
    merged = (
        sst.merge(sal, on="time", how="outer")
           .merge(chl, on="time", how="outer")
           .sort_values("time")
           .set_index("time")
           .resample("1D").mean()
           .interpolate(limit_direction="both")
           .reset_index()
    )

    # save
    out = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
    merged.to_csv(out, index=False)

    print(f"✅ Preprocessed saved → {out}")
    print(f"📊 Rows: {len(merged)}, Columns: {len(merged.columns)}")

    return merged


# ======================================
# CLI ENTRY POINT
# ======================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    preprocess_data(args.lat, args.lon)
