# data_fetchers/nightlights.py
import os, csv, math
import numpy as np
from utils.config import DATA_DIR

CSV = os.path.join(DATA_DIR, "synthetic_nightlights.csv")
_rows = None

def _load():
    global _rows
    if _rows is not None:
        return
    arr = []
    with open(CSV, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            arr.append((float(row["lat"]), float(row["lon"]), float(row["radiance"])))
    _rows = np.array(arr, dtype=float)

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    a = math.radians(lat1); b = math.radians(lon1)
    c = math.radians(lat2); d = math.radians(lon2)
    dlat = c - a; dlon = d - b
    aa = math.sin(dlat/2)**2 + math.cos(a)*math.cos(c)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(aa))

def get_nightlight(lat, lon, radius_km=50):
    _load()
    pts = _rows
    dists = np.vectorize(lambda rlat, rlon: _haversine(lat, lon, rlat, rlon))(pts[:,0], pts[:,1])
    mask = dists <= radius_km
    if mask.sum() == 0:
        return 0.0
    return float(np.mean(pts[mask,2]))

# compatibility alias
def count_nightlight(lat, lon, radius_km=50):
    return get_nightlight(lat, lon, radius_km)
