# # import requests
# # from utils.config import GEOAPIFY_KEY

# # def count_industries(lat, lon, radius_m=5000, timeout=10):
# #     """
# #     Use Geoapify Places API to count industry category objects around a point.
# #     Returns integer count or 0 on failure.
# #     """
# #     if not GEOAPIFY_KEY or GEOAPIFY_KEY.startswith("YOUR_"):
# #         # No key provided: return 0 so pipeline still runs
# #         return 0

# #     try:
# #         url = (
# #             "https://api.geoapify.com/v2/places?"
# #             f"categories=industry&filter=circle:{lon},{lat},{radius_m}"
# #             f"&limit=200&apiKey={GEOAPIFY_KEY}"
# #         )
# #         r = requests.get(url, timeout=timeout)
# #         if r.status_code == 200:
# #             return len(r.json().get("features", []))
# #     except Exception:
# #         pass
# #     return 0













# # data_fetchers/industries.py
# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_industries.csv")
# _rows = None

# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), int(row["industry_count"])))
#     _rows = np.array(arr, dtype=float)

# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     a = math.radians(lat1); b = math.radians(lon1)
#     c = math.radians(lat2); d = math.radians(lon2)
#     dlat = c - a; dlon = d - b
#     aa = math.sin(dlat/2)**2 + math.cos(a)*math.cos(c)*math.sin(dlon/2)**2
#     return 2*R*math.asin(math.sqrt(aa))

# def count_industries(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(lambda rlat, rlon: _haversine(lat, lon, rlat, rlon))(pts[:,0], pts[:,1])
#     mask = dists <= radius_km
#     return int(np.sum(pts[mask,2]))

# # alias
# def get_industry_count(lat, lon, radius_km=50):
#     return count_industries(lat, lon, radius_km)






# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_industries.csv")
# _rows = None


# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), float(row["industry_count"])))
#     _rows = np.array(arr, dtype=float)


# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     return 2*R*math.asin(math.sqrt(
#         math.sin((lat2-lat1)/2)**2 +
#         math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
#     ))


# def count_industries(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(
#         lambda rlat, rlon: _haversine(lat, lon, rlat, rlon)
#     )(pts[:, 0], pts[:, 1])
#     return float(np.sum(pts[dists <= radius_km, 2]))




















# data_fetchers/industries.py
import os, csv, math
import numpy as np
from utils.config import DATA_DIR

CSV = os.path.join(DATA_DIR, "synthetic_industries.csv")
_rows = None

def _load():
    """
    Loads synthetic_industries.csv
    Expected columns: lat, lon, industries_count
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
                int(row["industries_count"])
            ])
    _rows = np.array(arr)

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1 = np.radians([lat1, lon1])
    lat2, lon2 = np.radians([lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (np.sin(dlat/2)**2 +
         np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2)
    return 2 * R * np.arcsin(np.sqrt(a))

def count_industries(lat, lon, radius_km=50):
    _load()
    pts = _rows
    dists = _haversine(lat, lon, pts[:,0], pts[:,1])
    return int(np.sum(pts[dists <= radius_km, 2]))

# alias
get_industry_count = count_industries
