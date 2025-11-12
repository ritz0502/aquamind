# # utils.py
# import os
# import json
# import math
# import hashlib
# from pathlib import Path
# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans

# CACHE_DIR = Path("data/cache")
# CACHE_DIR.mkdir(parents=True, exist_ok=True)

# def cache_get(key: str):
#     """Return cached JSON for key or None."""
#     fname = CACHE_DIR / (hashlib.sha1(key.encode()).hexdigest() + ".json")
#     if not fname.exists():
#         return None
#     try:
#         with open(fname, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception:
#         return None

# def cache_set(key: str, obj):
#     """Cache JSON-serializable object under key."""
#     fname = CACHE_DIR / (hashlib.sha1(key.encode()).hexdigest() + ".json")
#     with open(fname, "w", encoding="utf-8") as f:
#         json.dump(obj, f)

# def make_key(prefix: str, **kwargs):
#     s = prefix + "|" + "|".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
#     return s

# def haversine(lon1, lat1, lon2, lat2):
#     # returns meters
#     R = 6371000.0
#     phi1, phi2 = math.radians(lat1), math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)
#     a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
#     return 2 * R * math.asin(math.sqrt(a))

# def grid_from_bbox(min_lat, min_lon, max_lat, max_lon, step_m=5000):
#     """
#     Create grid points within bbox with approximate step in meters (along lat/lon).
#     step_m ~ approximate spacing between points (uses latitude degrees conversion).
#     Return list of (lat, lon).
#     """
#     # approximate meters per degree lat/lon
#     # 1 deg lat ~ 111320 m
#     lat_step = step_m / 111320.0
#     # lon step depends on latitude (use center latitude)
#     mid_lat = (min_lat + max_lat) / 2.0
#     lon_meter = 111320.0 * math.cos(math.radians(mid_lat))
#     lon_step = step_m / max(lon_meter, 1e-6)
#     lats = np.arange(min_lat, max_lat + 1e-9, lat_step)
#     lons = np.arange(min_lon, max_lon + 1e-9, lon_step)
#     pts = []
#     for la in lats:
#         for lo in lons:
#             pts.append((float(la), float(lo)))
#     return pts

# def compute_activity_score_array(ports, industries, hotels):
#     raw = np.array(ports, dtype=float)*2 + np.array(industries, dtype=float)*3 + np.array(hotels, dtype=float)*1
#     mn = raw.min() if hasattr(raw, "min") else float(raw)
#     mx = raw.max() if hasattr(raw, "max") else float(raw)
#     if mx == mn:
#         return np.zeros_like(raw, dtype=float)
#     return (raw - mn) / (mx - mn)

# def spatial_groups(latlons, n_groups=5, random_state=42):
#     """
#     Create spatial group labels for spatial cross-validation.
#     Uses KMeans clustering on lat/lon.
#     """
#     arr = np.array(latlons)
#     if arr.shape[0] <= n_groups:
#         return np.arange(arr.shape[0])
#     km = KMeans(n_clusters=n_groups, random_state=random_state)
#     groups = km.fit_predict(arr)
#     return groups














































# utils.py
import os, json, hashlib

def make_key(prefix, **kwargs):
    key = f"{prefix}_" + "_".join([f"{k}-{v}" for k,v in kwargs.items()])
    return hashlib.md5(key.encode()).hexdigest()

def cache_get(key, folder="data/cache"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{key}.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def cache_set(key, data, folder="data/cache"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{key}.json")
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"⚠️ Cache write failed: {e}")
