import os
import argparse
import pandas as pd
import numpy as np
<<<<<<< HEAD
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

# MUST SAVE WHERE PROPHET EXPECTS
=======
from datetime import datetime, timedelta
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_and_clean_csv(file_path, variable_name):
<<<<<<< HEAD
    """Load raw CSV, clean it, and return standardized format."""
    if not os.path.exists(file_path):
        print(f"⚠️ File missing: {file_path}")
=======
    """
    Load a CSV file, parse time, and clean missing data.
    """
    if not os.path.exists(file_path):
        print(f"⚠️  File missing: {file_path}")
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
        return pd.DataFrame(columns=["time", variable_name])

    try:
        df = pd.read_csv(file_path)
        if "time" not in df.columns:
            raise ValueError("Missing 'time' column")

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
<<<<<<< HEAD
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
=======
        df = df.dropna(subset=["time"])

        # If variable name exists, clean it
        if variable_name in df.columns:
            df = df[["time", variable_name]]
        else:
            # Try to find closest-matching column name
            cols = [c for c in df.columns if variable_name.lower() in c.lower()]
            if cols:
                df.rename(columns={cols[0]: variable_name}, inplace=True)
                df = df[["time", variable_name]]
            else:
                print(f"⚠️  Variable '{variable_name}' not found in {file_path}")
                df[variable_name] = np.nan

        # Drop duplicates and sort by time
        df = df.drop_duplicates(subset=["time"]).sort_values("time")
        df = df.reset_index(drop=True)

        # Fill missing values by linear interpolation
        df[variable_name] = df[variable_name].interpolate(method="linear", limit_direction="both")
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8

        return df

    except Exception as e:
<<<<<<< HEAD
        print(f"❌ Failed to read/clean {file_path}: {e}")
=======
        print(f"❌ Failed to load {file_path}: {e}")
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
        return pd.DataFrame(columns=["time", variable_name])


def preprocess_data(lat, lon):
<<<<<<< HEAD
=======
    """
    Load and merge all marine datasets for given coordinates.
    """

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    print("\n==============================")
    print("🌊 MARINE DATA PREPROCESSOR")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print("==============================")

<<<<<<< HEAD
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
=======
    # File paths
    sst_path = os.path.join(RAW_DIR, f"open_meteo_{lat}_{lon}.csv")
    sal_path = os.path.join(RAW_DIR, f"salinity_{lat}_{lon}.csv")
    chl_path = os.path.join(RAW_DIR, f"chlor_a_{lat}_{lon}.csv")

    # Load datasets
    sst_df = load_and_clean_csv(sst_path, "sea_surface_temperature_max")
    sal_df = load_and_clean_csv(sal_path, "salinity")
    chl_df = load_and_clean_csv(chl_path, "chlor_a")

    # Merge all by time (outer join)
    merged = pd.merge(sst_df, sal_df, on="time", how="outer")
    merged = pd.merge(merged, chl_df, on="time", how="outer")

    # Fill missing with interpolation
    merged = merged.sort_values("time").reset_index(drop=True)
    merged = merged.set_index("time").resample("1D").mean().interpolate(limit_direction="both")
    
    # Ensure SST is numeric
    if "sea_surface_temperature_max" in merged.columns:
        merged["sea_surface_temperature_max"] = pd.to_numeric(
            merged["sea_surface_temperature_max"], errors="coerce"
        )

    # If still all NaN, fill with its mean
    if merged["sea_surface_temperature_max"].isna().all():
        print("⚠️  No valid SST values — filling with regional mean.")
        merged["sea_surface_temperature_max"].fillna(
            merged["sea_surface_temperature_max"].mean(), inplace=True
        )

    # Add derived features
    if "sea_surface_temperature_max" in merged.columns:
        merged["sst_rolling_mean_7d"] = merged["sea_surface_temperature_max"].rolling(7, min_periods=1).mean()
        merged["sst_anomaly"] = merged["sea_surface_temperature_max"] - merged["sst_rolling_mean_7d"]

    if "salinity" in merged.columns:
        merged["salinity_rolling_mean_7d"] = merged["salinity"].rolling(7, min_periods=1).mean()

    if "chlor_a" in merged.columns:
        merged["chlor_a_rolling_mean_7d"] = merged["chlor_a"].rolling(7, min_periods=1).mean()
        merged["chlor_a_rate"] = merged["chlor_a"].pct_change().fillna(0)

    # Save processed file
    out_path = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
    merged.to_csv(out_path)

    print(f"\n✅ Preprocessed dataset saved → {out_path}")
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    print(f"📊 Rows: {len(merged)}, Columns: {len(merged.columns)}")

    return merged


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    preprocess_data(args.lat, args.lon)
