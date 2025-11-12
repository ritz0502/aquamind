# # fetch_satellite.py
# import os
# import json
# import hashlib
# import numpy as np
# from pathlib import Path
# from utils import cache_get, cache_set, make_key

# # For Sentinel-5P download & query
# from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
# import datetime

# DATAHUB_URL = "https://apihub.copernicus.eu/apihub"  # or new Data Space API endpoint
# USERNAME = "kmehta3"
# PASSWORD = "Kriya@123"

# def get_no2_label_sentinel5p(lat, lon, date=None, radius_km=5):
#     """
#     Fetch tropospheric NO2 column value for given lat/lon (and date) from Sentinel-5P TROPOMI.
#     Requires Sentinelsat account (Copernicus). Returns numeric value (mol/m2) or None.
#     """
#     key = make_key("sat_no2", lat=lat, lon=lon, date=date, radius_km=radius_km)
#     cached = cache_get(key)
#     if cached is not None:
#         return cached

#     api = SentinelAPI(USERNAME, PASSWORD, DATAHUB_URL)
#     import datetime

#     if date is None:
#         # Default: yesterday
#         date_obj = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
#     else:
#         # If user provided date as string (YYYY-MM-DD), convert properly
#         if isinstance(date, str):
#             try:
#                 date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
#             except ValueError:
#                 date_obj = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
#         else:
#             date_obj = date

#     # Format for Sentinelsat (YYYYMMDD)
#     date_str = date_obj.strftime("%Y%m%d")


#     footprint = f"POINT({lon} {lat})"
#     # Query for Sentinel-5P NO2 products
#     products = api.query(
#         footprint,
#         date=(date_str, date_str),
#         platformname="Sentinel-5P",
#         producttype="L2__NO2___",  # approximate product type name
#         filename="*NO2*.nc"
#     )
#     if not products:
#         cache_set(key, None)
#         return None

#     # pick first
#     first_id = list(products.keys())[0]
#     api.download(first_id, directory_path="data/satellite_downloads")

#     # locate file
#     local_path = os.path.join("data/satellite_downloads", f"{first_id}.zip")  # or .nc
#     # User must unzip/convert to netCDF and sample the point.
#     # For simplicity we assume user extracts netCDF and we open via netCDF4 or rasterio
#     try:
#         import netCDF4
#         ds = netCDF4.Dataset(local_path.replace(".zip",".nc"))
#         # variable name: tropospheric_NO2_column_number_density
#         var = ds.variables["tropospheric_NO2_column_number_density"]
#         # approximate nearest index for lat/lon (optionally using variable lat/lon arrays)
#         # For simplicity take median value
#         arr = var[:]
#         val = float(np.nanmean(arr))
#         cache_set(key, val)
#         return val
#     except Exception as e:
#         print("❌ Reading Sentinel-5P NO2 file failed:", e)
#         cache_set(key, None)
#         return None

# def get_satellite_label_from_local_files(lat, lon, product_files, varname="target_var"):
#     """
#     (unchanged) sample from local raster/NetCDF files.
#     """
#     key = make_key("sat_local", lat=lat, lon=lon, files=";".join(product_files), var=varname)
#     cached = cache_get(key)
#     if cached is not None:
#         return cached

#     try:
#         import rasterio
#     except ImportError:
#         raise RuntimeError("rasterio not available")

#     for f in product_files:
#         try:
#             with rasterio.open(f) as src:
#                 rowcol = src.index(lon, lat)
#                 val = src.read(1)[rowcol]
#                 if val is None:
#                     continue
#                 if hasattr(src, "nodata") and val == src.nodata:
#                     continue
#                 valf = float(val)
#                 cache_set(key, valf)
#                 return valf
#         except Exception:
#             continue
#     return None

# def get_satellite_label(lat, lon, date=None, radius_km=5, product_files=None):
#     """
#     Unified call: if product_files provided, try local; else use Sentinel-5P NO2 fetch.
#     Returns numeric value or None.
#     """
#     # try local files first
#     if product_files:
#         val = get_satellite_label_from_local_files(lat, lon, product_files)
#         if val is not None:
#             return val

#     # fallback to Sentinel-5P NO2
#     return get_no2_label_sentinel5p(lat, lon, date=date, radius_km=radius_km)



































# fetch_satellite.py
import os
import subprocess
import xarray as xr
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import make_key, cache_get, cache_set

def _cache_safe(obj):
    """Convert any timestamps to string for JSON safety."""
    if isinstance(obj, pd.DataFrame):
        obj = obj.astype(str)
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {k: str(v) for k, v in obj.items()}
    else:
        return str(obj)

def fetch_copernicus_variable(variable, lat, lon, start_date, end_date, out_csv):
    """
    Fetch chlorophyll-a or salinity from Copernicus Marine (CLI).
    Uses caching; requires prior `copernicusmarine login`.
    """
    dataset_ids = {
        "chlor_a": {
            "id": "cmems_obs-oc_glo_bgc-plankton_nrt_l4-gapfree-multi-4km_P1D",
            "var": "CHL"
        },
        "salinity": {
            "id": "cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m",
            "var": "so"
        }
    }

    if variable not in dataset_ids:
        raise ValueError(f"Unsupported variable '{variable}'")

    dsid = dataset_ids[variable]["id"]
    varname = dataset_ids[variable]["var"]

    key = make_key("cmems", var=variable, lat=lat, lon=lon,
                   start=start_date, end=end_date)
    cached = cache_get(key)
    if cached:
        return pd.DataFrame(cached)

    folder = os.path.dirname(out_csv)
    os.makedirs(folder, exist_ok=True)
    print(f"🌊 Fetching {variable.upper()} for {lat:.2f},{lon:.2f}")

    cmd = [
        "copernicusmarine", "subset",
        "--dataset-id", dsid,
        "--variable", varname,
        "--start-datetime", f"{start_date}T00:00:00",
        "--end-datetime", f"{end_date}T23:59:59",
        "--minimum-latitude", str(lat - 0.25),
        "--maximum-latitude", str(lat + 0.25),
        "--minimum-longitude", str(lon - 0.25),
        "--maximum-longitude", str(lon + 0.25),
        "--file-format", "netcdf",
        "--output-directory", folder,
        "--overwrite", "--disable-progress-bar"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        nc_files = [f for f in os.listdir(folder)
                    if dsid in f and f.endswith(".nc")]
        if not nc_files:
            raise FileNotFoundError("No NetCDF file produced.")
        nc_path = os.path.join(folder, nc_files[-1])
        ds = xr.open_dataset(nc_path)
        df = ds.to_dataframe().reset_index()

        if varname not in df.columns:
            raise KeyError(f"{varname} missing in dataset.")

        df.rename(columns={varname: variable}, inplace=True)
        df = df[["time", variable]]
        df.to_csv(out_csv, index=False)
        ds.close()
        os.remove(nc_path)

        cache_set(key, _cache_safe(df))
        print(f"✅ Saved {variable} → {out_csv}")
        return df

    except Exception as e:
        print(f"❌ Copernicus fetch failed: {e}")
        return None


def fetch_many_points(variable, coords, start_date, end_date, base_folder="data"):
    """
    Parallel version for multiple coordinates.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(
                fetch_copernicus_variable,
                variable,
                lat, lon,
                start_date, end_date,
                os.path.join(base_folder, f"tmp_{lat}_{lon}.csv")
            ): (lat, lon)
            for lat, lon in coords
        }
        for fut in as_completed(futures):
            lat, lon = futures[fut]
            try:
                df = fut.result()
                results[(lat, lon)] = df
            except Exception as e:
                print(f"⚠️  {lat:.2f},{lon:.2f} failed: {e}")
    return results
