


# import os
# import argparse
# import pandas as pd
# from erddapy import ERDDAP
# import requests
# from datetime import datetime, timedelta, timezone

# # -------------------------------
# # 📂 Directory setup
# # -------------------------------
# DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# RAW_DIR = os.path.join(DATA_DIR, "raw")
# os.makedirs(RAW_DIR, exist_ok=True)


# # -------------------------------
# # 🌊 Fetch SST from NOAA ERDDAP
# # -------------------------------
# def fetch_erddap_point(server_url, dataset_id, var_name, lat, lon, start_date, end_date, out_csv):
#     """
#     Fetch daily sea surface temperature data for a specific lat/lon and date range
#     from an ERDDAP griddap dataset (CSV format).
#     """
#     from erddapy import ERDDAP

#     e = ERDDAP(server=server_url)
#     e.protocol = "griddap"
#     e.dataset_id = dataset_id

#     # initialize metadata before constraints
#     e.griddap_initialize()

#     # now safely set constraints
#     e.constraints = {
#         "time>=": start_date,
#         "time<=": end_date,
#         "latitude>=": lat,
#         "latitude<=": lat,
#         "longitude>=": lon,
#         "longitude<=": lon
#     }

#     e.variables = ["time", var_name]
#     e.response = "csv"

#     csv_url = e.get_download_url()
#     print(f"\n🌍 Fetching SST from ERDDAP:\n{csv_url}\n")

#     try:
#         df = pd.read_csv(csv_url)
#         if df.empty:
#             raise ValueError("Empty dataframe received from ERDDAP. Check dataset ID and coordinates.")
#         df.to_csv(out_csv, index=False)
#         print(f"✅ Saved SST data to: {out_csv}\n")
#         return out_csv
#     except Exception as e:
#         print(f"❌ ERDDAP fetch failed: {e}\n")
#         raise


# # -------------------------------
# # 🌤 Fetch Marine Data from Open-Meteo
# # -------------------------------
# def fetch_open_meteo(lat, lon, start_date, end_date, out_csv):
#     """
#     Fetch daily marine weather metrics from Open-Meteo Marine API (no key needed).
#     Includes sea surface temp, wind speed, and wave height.
#     """
#     base = "https://marine-api.open-meteo.com/v1/marine"
#     params = {
#         "latitude": lat,
#         "longitude": lon,
#         "start_date": start_date,
#         "end_date": end_date,
#         "daily": "sea_surface_temperature_max,sea_surface_temperature_min,wind_speed_10m_max,wave_height_max",
#         "timezone": "UTC"
#     }

#     print(f"\n🌊 Fetching marine data from Open-Meteo for {start_date} → {end_date}")
#     print(f"Endpoint: {base}\n")

#     r = requests.get(base, params=params)
#     r.raise_for_status()
#     j = r.json()

#     daily = j.get("daily", {})
#     if not daily:
#         raise RuntimeError("Open-Meteo returned no daily data. Check date range or parameters.")

#     df = pd.DataFrame(daily)
#     df["time"] = pd.to_datetime(df["time"])
#     df.to_csv(out_csv, index=False)
#     print(f"✅ Saved Open-Meteo marine data to: {out_csv}\n")
#     return out_csv


# # -------------------------------
# # 🚀 Main runner
# # -------------------------------
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Fetch SST + marine data for given coordinates and date range.")
#     parser.add_argument("--lat", type=float, required=True, help="Latitude of location")
#     parser.add_argument("--lon", type=float, required=True, help="Longitude of location")
#     parser.add_argument("--days", type=int, default=60, help="Number of past days to fetch")
#     args = parser.parse_args()

#     # Time range setup (UTC)
#     end = datetime.now(timezone.utc).date()
#     start = end - timedelta(days=args.days)
#     start_str = start.isoformat()
#     end_str = end.isoformat()

#     print("\n==============================")
#     print("🌎 MARINE RISK DATA FETCHER")
#     print("==============================")
#     print(f"Latitude: {args.lat} | Longitude: {args.lon}")
#     print(f"Date range: {start_str} → {end_str}")
#     print("==============================\n")

#     # ---- Fetch SST from ERDDAP ----
#     try:
#         server = "https://coastwatch.pfeg.noaa.gov/erddap"
#         dataset_id = "ncdcOisst21Agg_LonPM180"
#         var_name = "sst"
#         out_sst = os.path.join(RAW_DIR, f"sst_{args.lat}_{args.lon}_{start_str}_{end_str}.csv")
#         fetch_erddap_point(server, dataset_id, var_name, args.lat, args.lon, start_str, end_str, out_sst)
#     except Exception as e:
#         print(f"⚠️ Skipping ERDDAP SST due to error: {e}")

#     # ---- Fetch Marine data from Open-Meteo ----
#     try:
#         out_om = os.path.join(RAW_DIR, f"open_meteo_{args.lat}_{args.lon}_{start_str}_{end_str}.csv")
#         fetch_open_meteo(args.lat, args.lon, start_str, end_str, out_om)
#     except Exception as e:
#         print(f"⚠️ Skipping Open-Meteo due to error: {e}")

#     print("\n✅ Data fetching complete! Check the 'data/raw' folder for downloaded CSV files.\n")





















import os
import argparse
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)


# def fetch_open_meteo(lat, lon, start_date, end_date, out_csv):
#     """Fetch SST, wind, wave from Open-Meteo Marine (always works)."""
#     url = "https://marine-api.open-meteo.com/v1/marine"
#     params = {
#         "latitude": lat,
#         "longitude": lon,
#         "start_date": start_date,
#         "end_date": end_date,
#         "daily": "sea_surface_temperature_max,sea_surface_temperature_min,wind_speed_10m_max,wave_height_max",
#         "timezone": "UTC",
#     }
#     print(f"\n🌊 Fetching Open-Meteo Marine data {start_date}→{end_date}")
#     r = requests.get(url, params=params, timeout=30)
#     r.raise_for_status()
#     data = r.json().get("daily", {})
#     if not data:
#         raise RuntimeError("No Open-Meteo data returned")
#     df = pd.DataFrame(data)
#     df["time"] = pd.to_datetime(df["time"])
#     df.to_csv(out_csv, index=False)
#     print(f"✅ Saved Open-Meteo data → {out_csv}")
#     return df


import time
import requests
import pandas as pd

def fetch_open_meteo(lat, lon, start_date, end_date, out_csv, max_retries=5):
    """Fetch SST, wind, wave from Open-Meteo Marine with retries and fallback."""
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "sea_surface_temperature_max,sea_surface_temperature_min,wind_speed_10m_max,wave_height_max",
        "timezone": "UTC",
    }

    print(f"\n🌊 Fetching Open-Meteo Marine data {start_date}→{end_date}")

    for attempt in range(1, max_retries + 1):
        try:
            # Exponential backoff in case of API lag
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()
            data = r.json().get("daily", {})
            if not data:
                raise RuntimeError("No Open-Meteo data returned")
            df = pd.DataFrame(data)
            df["time"] = pd.to_datetime(df["time"])
            df.to_csv(out_csv, index=False)
            print(f"✅ Saved Open-Meteo data → {out_csv}")
            return df

        except requests.exceptions.Timeout:
            print(f"⚠️ Open-Meteo timeout (attempt {attempt}/{max_retries})")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Network connection error (attempt {attempt}/{max_retries})")
        except Exception as e:
            print(f"⚠️ Open-Meteo fetch error ({attempt}/{max_retries}): {e}")

        # Wait before retrying (exponential backoff)
        time.sleep(5 * attempt)

    # Fallback: write placeholder CSV to keep pipeline running
    print("❌ Open-Meteo API unreachable after multiple attempts. Writing placeholder CSV.")
    pd.DataFrame({
        "time": pd.date_range(start=start_date, end=end_date, freq="D"),
        "sea_surface_temperature_max": None,
        "sea_surface_temperature_min": None,
        "wind_speed_10m_max": None,
        "wave_height_max": None
    }).to_csv(out_csv, index=False)
    return None



# def fetch_copernicus_variable(variable, lat, lon, start_date, end_date, out_csv):
#     """
#     Fetch surface salinity or chlorophyll from Copernicus Marine via public subset service.
#     """
#     base_urls = {
#         "salinity": "https://nrt.cmems-du.eu/api/subset?dataset-id=cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m",
#         "chlor_a": "https://nrt.cmems-du.eu/api/subset?dataset-id=cmems_mod_glo_bgc-chl_anfc_0.25deg_P1D-m",
#     }
#     if variable not in base_urls:
#         raise ValueError("Unsupported variable")
#     params = {
#         "variables": variable,
#         "north": lat + 0.25,
#         "south": lat - 0.25,
#         "east": lon + 0.25,
#         "west": lon - 0.25,
#         "start-datetime": f"{start_date}T00:00:00Z",
#         "end-datetime": f"{end_date}T00:00:00Z",
#         "format": "json"
#     }
#     url = base_urls[variable]
#     print(f"\n🌍 Fetching {variable} from Copernicus Marine")
#     r = requests.get(url, params=params, timeout=60)
#     if r.status_code != 200:
#         print(f"⚠️ Copernicus returned {r.status_code}, writing placeholder CSV.")
#         pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)
#         return None
#     j = r.json()
#     if not j or "data" not in j:
#         print(f"⚠️ No {variable} data found, writing placeholder.")
#         pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)
#         return None
#     df = pd.DataFrame(j["data"])
#     if "time" not in df.columns:
#         df.rename(columns={df.columns[0]: "time"}, inplace=True)
#     df["time"] = pd.to_datetime(df["time"])
#     df.to_csv(out_csv, index=False)
#     print(f"✅ Saved {variable} → {out_csv}")
#     return df


import subprocess
import pandas as pd
import os
import xarray as xr

def fetch_copernicus_variable(variable, lat, lon, start_date, end_date, out_csv):
    """
    Fetch real chlorophyll-a or salinity from Copernicus Marine authenticated API.
    Uses global datasets and converts NetCDF → CSV automatically.
    """

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

    print(f"\n🌍 Fetching {variable} ({dataset_var}) via Copernicus Marine (authenticated)...")

    try:
        cmd = [
            "copernicusmarine", "subset",
            "--dataset-id", dataset,
            "--variable", dataset_var,
            "--start-datetime", f"{start_date}T00:00:00",
            "--end-datetime", f"{end_date}T00:00:00",
            "--minimum-latitude", str(lat - 0.25),
            "--maximum-latitude", str(lat + 0.25),
            "--minimum-longitude", str(lon - 0.25),
            "--maximum-longitude", str(lon + 0.25),
            "--file-format", "netcdf",
            "--output-directory", os.path.dirname(out_csv),
            "--overwrite",
            "--disable-progress-bar"
        ]

        subprocess.run(cmd, check=True)

        folder = os.path.dirname(out_csv)
        nc_files = [f for f in os.listdir(folder) if dataset in f and f.endswith(".nc")]
        if not nc_files:
            raise FileNotFoundError("No NetCDF file found after Copernicus fetch")

        nc_path = os.path.join(folder, nc_files[-1])

        # Convert NetCDF → CSV
        ds = xr.open_dataset(nc_path)
        df = ds.to_dataframe().reset_index()

        # Keep time + main variable
        if dataset_var in df.columns:
            df.rename(columns={dataset_var: variable}, inplace=True)
            df = df[["time", variable]]
        else:
            raise KeyError(f"Variable '{dataset_var}' not found in dataset columns")

        df.to_csv(out_csv, index=False)
        ds.close()
        os.remove(nc_path)

        print(f"✅ Saved Copernicus {variable} → {out_csv}")

    except Exception as e:
        print(f"❌ Failed to fetch {variable}: {e}")
        pd.DataFrame({"time": [], variable: []}).to_csv(out_csv, index=False)



def main(lat, lon, days):
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)
    start_str, end_str = start.isoformat(), end.isoformat()

    print("\n==============================")
    print("🌎 MARINE RISK DATA FETCHER (full-proof)")
    print("==============================")
    print(f"Coordinates: ({lat}, {lon})")
    print(f"Date range : {start_str} → {end_str}")
    print("==============================")

    # 1️⃣ SST, wind, wave
    fetch_open_meteo(
        lat, lon, start_str, end_str,
        os.path.join(RAW_DIR, f"open_meteo_{lat}_{lon}.csv")
    )

    # 2️⃣ Salinity
    fetch_copernicus_variable(
        "salinity", lat, lon, start_str, end_str,
        os.path.join(RAW_DIR, f"salinity_{lat}_{lon}.csv")
    )

    # 3️⃣ Chlorophyll-a
    fetch_copernicus_variable(
        "chlor_a", lat, lon, start_str, end_str,
        os.path.join(RAW_DIR, f"chlor_a_{lat}_{lon}.csv")
    )

    print("\n✅ All data fetched successfully (or placeholders created).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--days", type=int, default=60)
    args = parser.parse_args()
    main(args.lat, args.lon, args.days)
