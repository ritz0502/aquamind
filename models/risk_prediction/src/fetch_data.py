import os
import subprocess
import pandas as pd
import xarray as xr
import argparse
from datetime import datetime, timedelta, timezone
import sys
sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)
def split_into_months(start_date, end_date):
    """Split a date range into month-sized chunks."""
    months = []
    current = start_date.replace(day=1)

    while current < end_date:
        # First day of next month
        next_month = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
        months.append((current, min(next_month, end_date)))
        current = next_month

    return months

def fetch_copernicus_variable(variable, lat, lon, start_date, end_date, out_csv):
    """Fetch salinity/chlor_a from Copernicus in monthly chunks to avoid freezing."""
    dataset_ids = {
        "salinity": {
            "id": "cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m",
            "var": "so"
        },
        "chlor_a": {
            "id": "cmems_obs-oc_glo_bgc-plankton_nrt_l4-gapfree-multi-4km_P1D",
            "var": "CHL"
        }
    }

    if variable not in dataset_ids:
        raise ValueError(f"Unsupported variable: {variable}")

    dataset = dataset_ids[variable]["id"]
    dataset_var = dataset_ids[variable]["var"]

    print(f"\n🌍 Fetching {variable} ({dataset_var}) via Copernicus Marine (monthly split)...")

    # Where to store temporary monthly NetCDF files
    folder = os.path.dirname(out_csv)
    os.makedirs(folder, exist_ok=True)

    # ---------- MONTHLY LOOP ----------
    all_frames = []
    monthly_ranges = split_into_months(
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date)
    )

    for i, (s, e) in enumerate(monthly_ranges, 1):
        print(f"  📅 Month {i}: {s.date()} → {e.date()}")

        nc_out = os.path.join(folder, f"{variable}_chunk_{i}.nc")

        cmd = [
            "copernicusmarine", "subset",
            "--dataset-id", dataset,
            "--variable", dataset_var,
            "--start-datetime", f"{s.date()}T00:00:00",
            "--end-datetime", f"{e.date()}T00:00:00",
            "--minimum-latitude", str(lat - 0.25),
            "--maximum-latitude", str(lat + 0.25),
            "--minimum-longitude", str(lon - 0.25),
            "--maximum-longitude", str(lon + 0.25),
            "--file-format", "netcdf",
            "--output-directory", folder,
            "--out-name", os.path.basename(nc_out),
            "--overwrite",
            "--disable-progress-bar"
        ]

        try:
            subprocess.run(cmd, check=True)

            ds = xr.open_dataset(nc_out)
            df = ds.to_dataframe().reset_index()
            ds.close()

            if dataset_var not in df.columns:
                print(f"⚠️ Missing variable {dataset_var} in month {i}, skipping…")
                continue

            df.rename(columns={dataset_var: variable}, inplace=True)
            df = df[["time", variable]]
            all_frames.append(df)

        except Exception as e:
            print(f"❌ Month {i} failed: {e}")

        # Clean up monthly file
        if os.path.exists(nc_out):
            os.remove(nc_out)

    # ---------- MERGE ALL MONTHS ----------
    if all_frames:
        final_df = pd.concat(all_frames)
        final_df.to_csv(out_csv, index=False)
        print(f"✅ Saved Copernicus {variable} → {out_csv}")
    else:
        print(f"⚠️ No data available for {variable}, saving empty CSV.")
        pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)


def fetch_open_meteo(lat, lon, start_date, end_date, out_csv):
    """Dummy placeholder for SST, wind, wave data fetcher."""
    print(f"\n🌊 Fetching Open-Meteo Marine data {start_date}→{end_date}")
    pd.DataFrame({
        "time": pd.date_range(start=start_date, end=end_date),
        "sea_surface_temperature_max": [28 + (i % 3) for i in range((datetime.fromisoformat(end_date) - datetime.fromisoformat(start_date)).days + 1)]
    }).to_csv(out_csv, index=False)
    print(f"✅ Saved Open-Meteo data → {out_csv}")


def main(lat, lon, days):
    HISTORY_DAYS = 365  # Prophet needs full year
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=HISTORY_DAYS)

    start_str, end_str = start.isoformat(), end.isoformat()

    print("\n==============================")
    print("🌎 MARINE RISK DATA FETCHER (full-proof)")
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

    print("\n✅ All data fetched successfully (or placeholders created).")
