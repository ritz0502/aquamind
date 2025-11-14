import os
import argparse
import pandas as pd
import requests
import time
import subprocess
import xarray as xr
from datetime import datetime, timedelta, timezone
import sys
sys.stdout.reconfigure(encoding='utf-8')


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)


# ----------------------------------------------
# 1️⃣ OPEN-METEO FETCHER  (unchanged, stable)
# ----------------------------------------------
def fetch_open_meteo(lat, lon, start_date, end_date, out_csv, max_retries=5):
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "sea_surface_temperature_max",
        "timezone": "UTC",
    }

    print(f"\n🌊 Fetching Open-Meteo Marine data {start_date}→{end_date}")

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()
            data = r.json().get("daily", {})
            df = pd.DataFrame(data)
            df["time"] = pd.to_datetime(df["time"])
            df.to_csv(out_csv, index=False)
            print(f"✅ Saved Open-Meteo → {out_csv}")
            return
        except Exception as e:
            print(f"⚠️ Error attempt {attempt}: {e}")
            time.sleep(3)

    # Fallback dummy file
    print("❌ Failed Open-Meteo. Writing placeholder file.")
    dates = pd.date_range(start=start_date, end=end_date)
    pd.DataFrame({"time": dates, "sea_surface_temperature_max": [None] * len(dates)}).to_csv(out_csv, index=False)



# ------------------------------------------------------
# 2️⃣ COPERNICUS FETCHER — FIXED & STABLE VERSION
# ------------------------------------------------------

# Working dataset IDs:
SALINITY_DATASET = "cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m"
CHL_DATASET      = "cmems_obs-oc_glo_bgc-plankton_nrt_l4-gapfree-multi-4km_P1D"


def fetch_copernicus_variable(variable, lat, lon, start, end, out_csv):
    """Stable version identical to your older working script but fixed for new API."""

    datasets = {
        "salinity": {"id": SALINITY_DATASET, "var": "so"},
        "chlor_a":  {"id": CHL_DATASET, "var": "CHL"},
    }

    dataset = datasets[variable]["id"]
    var = datasets[variable]["var"]

    print(f"\n🌍 Fetching {variable} from Copernicus (dataset={dataset})")

    folder = os.path.dirname(out_csv)
    os.makedirs(folder, exist_ok=True)

    # Build CLI command
    cmd = [
        "copernicusmarine", "subset",
        "--dataset-id", dataset,
        "--variable", var,
        "--start-datetime", f"{start}T00:00:00",
        "--end-datetime", f"{end}T00:00:00",
        "--minimum-latitude", str(lat - 0.25),
        "--maximum-latitude", str(lat + 0.25),
        "--minimum-longitude", str(lon - 0.25),
        "--maximum-longitude", str(lon + 0.25),
        "--file-format", "netcdf",
        "--output-directory", folder,
        "--output-filename", f"{variable}_{lat}_{lon}.nc",
        "--overwrite",
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"❌ Copernicus failed: {e}")
        pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)
        return

    # Find downloaded .nc file
    nc_path = os.path.join(folder, f"{variable}_{lat}_{lon}.nc")
    if not os.path.exists(nc_path):
        print("❌ No .nc file downloaded — writing empty CSV.")
        pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)
        return

    # Read and convert to CSV
    try:
        ds = xr.open_dataset(nc_path)
        df = ds.to_dataframe().reset_index()
        ds.close()

        if var not in df.columns:
            print(f"⚠️ No column '{var}' found — writing empty CSV.")
            pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)
            return

        df.rename(columns={var: variable}, inplace=True)
        df = df[["time", variable]]
        df.to_csv(out_csv, index=False)
        print(f"✅ Saved {variable} → {out_csv}")

    except Exception as e:
        print(f"❌ Failed reading dataset: {e}")
        pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)

    # Remove nc file after extraction
    try:
        os.remove(nc_path)
    except:
        pass



# ----------------------------------------------
# 3️⃣ MAIN
# ----------------------------------------------
def main(lat, lon, days):
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)

    start_str, end_str = start.isoformat(), end.isoformat()

    print("\n==============================")
    print("🌎 MARINE DATA FETCHER (Stable)")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print(f"Date range : {start_str} → {end_str}")
    print("==============================")

    fetch_open_meteo(lat, lon, start_str, end_str,
                     os.path.join(RAW_DIR, f"open_meteo_{lat}_{lon}.csv"))

    fetch_copernicus_variable("salinity", lat, lon, start_str, end_str,
                              os.path.join(RAW_DIR, f"salinity_{lat}_{lon}.csv"))

    fetch_copernicus_variable("chlor_a", lat, lon, start_str, end_str,
                              os.path.join(RAW_DIR, f"chlor_a_{lat}_{lon}.csv"))

    print("\n✅ All data fetched.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--days", type=int, default=60)
    args = parser.parse_args()
    main(args.lat, args.lon, args.days)
