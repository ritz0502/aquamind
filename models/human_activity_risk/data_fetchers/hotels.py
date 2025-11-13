# # # data_fetchers/hotels.py

# # import requests
# # from utils.config import GEOAPIFY_KEY, HOTEL_RADIUS_M

# # def count_hotels(lat, lon):
# #     """
# #     Count hotels, resorts, guest houses, tourism accommodations 
# #     using Geoapify Places API.
# #     """
# #     if GEOAPIFY_KEY.startswith("YOUR_") or len(GEOAPIFY_KEY) < 5:
# #         return 0

# #     url = (
# #         "https://api.geoapify.com/v2/places?"
# #         "categories=accommodation.hotel|accommodation.resort|tourism&"
# #         f"filter=circle:{lon},{lat},{HOTEL_RADIUS_M}"
# #         "&bias=proximity:"
# #         f"{lon},{lat}&limit=200"
# #         f"&apiKey={GEOAPIFY_KEY}"
# #     )

# #     try:
# #         r = requests.get(url, timeout=8)
# #         if r.status_code == 200:
# #             return len(r.json().get("features", []))
# #     except Exception:
# #         pass

# #     return 0




















# # data_fetchers/hotels.py
# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_hotels.csv")
# _rows = None

# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), int(row["hotel_count"])))
#     _rows = np.array(arr, dtype=float)

# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     a = math.radians(lat1); b = math.radians(lon1)
#     c = math.radians(lat2); d = math.radians(lon2)
#     dlat = c - a; dlon = d - b
#     aa = math.sin(dlat/2)**2 + math.cos(a)*math.cos(c)*math.sin(dlon/2)**2
#     return 2*R*math.asin(math.sqrt(aa))

# def count_hotels(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(lambda rlat, rlon: _haversine(lat, lon, rlat, rlon))(pts[:,0], pts[:,1])
#     mask = dists <= radius_km
#     return int(np.sum(pts[mask,2]))

# # alias
# def get_hotel_count(lat, lon, radius_km=50):
#     return count_hotels(lat, lon, radius_km)








# import os, csv, math
# import numpy as np
# from utils.config import DATA_DIR

# CSV = os.path.join(DATA_DIR, "synthetic_hotels.csv")
# _rows = None


# def _load():
#     global _rows
#     if _rows is not None:
#         return
#     arr = []
#     with open(CSV, newline="") as f:
#         r = csv.DictReader(f)
#         for row in r:
#             arr.append((float(row["lat"]), float(row["lon"]), float(row["hotel_count"])))
#     _rows = np.array(arr, dtype=float)


# def _haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     return 2*R*math.asin(math.sqrt(
#         math.sin((lat2-lat1)/2)**2 +
#         math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
#     ))


# def count_hotels(lat, lon, radius_km=50):
#     _load()
#     pts = _rows
#     dists = np.vectorize(
#         lambda rlat, rlon: _haversine(lat, lon, rlat, rlon)
#     )(pts[:, 0], pts[:, 1])
#     return float(np.sum(pts[dists <= radius_km, 2]))


















# data_fetchers/hotels.py
import os, csv, math
import numpy as np
from utils.config import DATA_DIR

CSV = os.path.join(DATA_DIR, "synthetic_hotels.csv")
_rows = None

def _load():
    """
    Loads synthetic_hotels.csv
    Expected columns: lat, lon, hotels_count
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
                int(row["hotels_count"])
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

def count_hotels(lat, lon, radius_km=50):
    _load()
    pts = _rows
    dists = _haversine(lat, lon, pts[:,0], pts[:,1])
    return int(np.sum(pts[dists <= radius_km, 2]))

# alias
get_hotel_count = count_hotels
