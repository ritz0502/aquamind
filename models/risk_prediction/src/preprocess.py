import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_and_clean_csv(file_path, variable_name):
    """
    Load a CSV file, parse time, and clean missing data.
    """
    if not os.path.exists(file_path):
        print(f"⚠️  File missing: {file_path}")
        return pd.DataFrame(columns=["time", variable_name])

    try:
        df = pd.read_csv(file_path)
        if "time" not in df.columns:
            raise ValueError("Missing 'time' column")

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
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

        return df

    except Exception as e:
        print(f"❌ Failed to load {file_path}: {e}")
        return pd.DataFrame(columns=["time", variable_name])


def preprocess_data(lat, lon):
    """
    Load and merge all marine datasets for given coordinates.
    """

    print("\n==============================")
    print("🌊 MARINE DATA PREPROCESSOR")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print("==============================")

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
    print(f"📊 Rows: {len(merged)}, Columns: {len(merged.columns)}")

    return merged


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    preprocess_data(args.lat, args.lon)
