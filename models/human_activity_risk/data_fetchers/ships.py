# # import requests

# # def get_ship_density(lat, lon, radius_km=20, timeout=8):
# #     """
# #     Query AISStream public geojson endpoint for ship positions inside a radius (km).
# #     Returns integer count (0 if error).
# #     """
# #     try:
# #         url = f"https://stream.aisstream.io/v0/geojson?lat={lat}&lon={lon}&radius={radius_km}"
# #         r = requests.get(url, timeout=timeout)
# #         if r.status_code != 200:
# #             return 0
# #         data = r.json()
# #         features = data.get("features", [])
# #         return len(features)
# #     except Exception:
# #         return 0








# # data_fetchers/ships.py
# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_ships.csv")
# _rows = None

# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), int(row["ships"])))
#     _rows = np.array(arr, dtype=float)

# def _haversine(lat1, lon1, lat2, lon2):
#     # returns km
#     R = 6371.0
#     a = math.radians(lat1); b = math.radians(lon1)
#     c = math.radians(lat2); d = math.radians(lon2)
#     dlat = c - a; dlon = d - b
#     aa = math.sin(dlat/2)**2 + math.cos(a)*math.cos(c)*math.sin(dlon/2)**2
#     return 2*R*math.asin(math.sqrt(aa))

# def count_ships(lat, lon, radius_km=50):
#     """
#     Sum ships whose synthetic point is within radius_km of (lat,lon).
#     """
#     _load()
#     pts = _rows
#     dists = np.vectorize(lambda rlat, rlon: _haversine(lat, lon, rlat, rlon))(pts[:,0], pts[:,1])
#     mask = dists <= radius_km
#     return int(np.sum(pts[mask,2]))

# # alias for compatibility
# def get_ship_count(lat, lon, radius_km=50):
#     return count_ships(lat, lon, radius_km)


# def get_ship_density(lat, lon, radius_km=50):
#     return count_ships(lat, lon, radius_km)






# # data_fetchers/ships.py
# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_ships.csv")
# _rows = None


# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), float(row["ships"])))
#     _rows = np.array(arr, dtype=float)


# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     aa = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
#     return 2*R*math.asin(math.sqrt(aa))


# def get_ship_density(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(
#         lambda rlat, rlon: _haversine(lat, lon, rlat, rlon)
#     )(pts[:, 0], pts[:, 1])

#     return float(np.sum(pts[dists <= radius_km, 2]))
































import os, csv, math
import numpy as np
from utils.config import DATA_DIR

CSV = os.path.join(DATA_DIR, "synthetic_ships.csv")
_rows = None

def _load():
    global _rows
    if _rows is not None:
        return
    arr = []
    with open(CSV) as f:
        r = csv.DictReader(f)
        for row in r:
            arr.append([float(row["lat"]), float(row["lon"]), int(row["ships_count"])])
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

def get_ship_density(lat, lon, radius_km=50):
    _load()
    pts = _rows
    dists = _haversine(lat, lon, pts[:,0], pts[:,1])
    return int(np.sum(pts[dists <= radius_km, 2]))
