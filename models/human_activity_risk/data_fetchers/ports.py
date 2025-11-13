# import os
# import pandas as pd

# # Expect Kaggle CSV format with columns like: LATITUDE, LONGITUDE, PORT_NAME...
# CSV_PATH = os.path.join("data", "world_ports.csv")

# def _load_ports_df():
#     if not os.path.exists(CSV_PATH):
#         print("⚠️ world_ports.csv not found at data/world_ports.csv")
#         return pd.DataFrame(columns=["lat", "lon"])
#     df = pd.read_csv(CSV_PATH, dtype=str, low_memory=False)
#     # Normalize column names to lower case
#     df.columns = [c.strip().lower() for c in df.columns]

#     # Find which columns are lat/lon
#     lat_col = None
#     lon_col = None
#     for candidate in ("latitude", "lat", "y"):
#         if candidate in df.columns:
#             lat_col = candidate
#             break
#     for candidate in ("longitude", "lon", "lng", "x"):
#         if candidate in df.columns:
#             lon_col = candidate
#             break

#     if lat_col is None or lon_col is None:
#         # If columns not found, try to inspect 'coordinates' like fields
#         raise ValueError("Could not find latitude/longitude columns in world_ports.csv")

#     # convert to numeric and drop invalids
#     df = df[[lat_col, lon_col]].rename(columns={lat_col: "lat", lon_col: "lon"})
#     df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
#     df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
#     df = df.dropna(subset=["lat", "lon"]).reset_index(drop=True)
#     return df

# # Load once
# _PORTS_DF = _load_ports_df()

# def count_near_ports(lat, lon, radius_km=20):
#     """
#     Count ports in _PORTS_DF within radius_km of (lat, lon).
#     Uses simple box filter (fast) as approximation then exact haversine if desired.
#     """
#     if _PORTS_DF.empty:
#         return 0
#     # degree approx
#     d = radius_km / 111.0
#     subset = _PORTS_DF[
#         (_PORTS_DF.lat >= lat - d) & (_PORTS_DF.lat <= lat + d) &
#         (_PORTS_DF.lon >= lon - d) & (_PORTS_DF.lon <= lon + d)
#     ]
#     return int(len(subset))






# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_ports.csv")
# _rows = None


# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), float(row["ports"])))
#     _rows = np.array(arr, dtype=float)


# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     return 2*R*math.asin(math.sqrt(
#         math.sin((lat2-lat1)/2)**2 +
#         math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
#     ))


# def count_near_ports(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(
#         lambda rlat, rlon: _haversine(lat, lon, rlat, rlon)
#     )(pts[:, 0], pts[:, 1])
#     return float(np.sum(pts[dists <= radius_km, 2]))




















# data_fetchers/ports.py
import os, csv
import numpy as np
from utils.config import DATA_DIR

CSV = os.path.join(DATA_DIR, "synthetic_ports.csv")
_rows = None

def _load():
    """
    Loads synthetic_ports.csv
    Expected columns: lat, lon, ports_count
    """
    global _rows
    if _rows is not None:
        return

    arr = []
    with open(CSV, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            arr.append([
                float(row["lat"]),
                float(row["lon"]),
                int(row["ports_count"])
            ])
    _rows = np.array(arr)

def count_near_ports(lat, lon, radius_km=50):
    _load()

    # Fast filter using simple bounding box reduction
    deg = radius_km / 111
    pts = _rows

    subset = pts[
        (pts[:,0] >= lat - deg) &
        (pts[:,0] <= lat + deg) &
        (pts[:,1] >= lon - deg) &
        (pts[:,1] <= lon + deg)
    ]

    return int(np.sum(subset[:,2]))
