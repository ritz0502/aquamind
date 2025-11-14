import os
import argparse
import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

# MUST SAVE WHERE PROPHET EXPECTS
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


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
        df = df.dropna(subset=["time"]).sort_values("time")

        # Find variable column
        if variable_name not in df.columns:
            possible = [c for c in df.columns if variable_name.lower() in c.lower()]
            if possible:
                df.rename(columns={possible[0]: variable_name}, inplace=True)
            else:
                df[variable_name] = np.nan

        df = df[["time", variable_name]]
        df[variable_name] = pd.to_numeric(df[variable_name], errors="coerce")
        df[variable_name] = df[variable_name].interpolate(limit_direction="both")

        return df

    except Exception as e:
        print(f"❌ Failed to read/clean {file_path}: {e}")
        return pd.DataFrame(columns=["time", variable_name])


def preprocess_data(lat, lon):
    print("\n==============================")
    print("🌊 MARINE DATA PREPROCESSOR")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print("==============================")

    # RAW FILES
    sst_raw = os.path.join(RAW_DIR, f"open_meteo_{lat}_{lon}.csv")
    sal_raw = os.path.join(RAW_DIR, f"salinity_{lat}_{lon}.csv")
    chl_raw = os.path.join(RAW_DIR, f"chlor_a_{lat}_{lon}.csv")

    sst = load_and_clean_csv(sst_raw, "sea_surface_temperature_max")
    sal = load_and_clean_csv(sal_raw, "salinity")
    chl = load_and_clean_csv(chl_raw, "chlor_a")

    # MERGE
    merged = (
        sst.merge(sal, on="time", how="outer")
           .merge(chl, on="time", how="outer")
           .sort_values("time")
           .set_index("time")
           .resample("1D").mean()
           .interpolate(limit_direction="both")
           .reset_index()
    )

    # SAVE
    out = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
    merged.to_csv(out, index=False)

    print(f"✅ Preprocessed saved → {out}")
    print(f"📊 Rows: {len(merged)}, Columns: {len(merged.columns)}")

    return merged


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    preprocess_data(args.lat, args.lon)
