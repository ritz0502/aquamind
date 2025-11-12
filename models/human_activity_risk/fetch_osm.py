# # fetch_osm.py (keep as-is)
# import requests
# import time
# from typing import Tuple, List
# from utils import cache_get, cache_set, make_key

# OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# def _overpass_query_for_point(lat: float, lon: float, radius_m: int = 5000, timeout=60):
#     query = f"""
#     [out:json][timeout:{timeout}];
#     (
#       node(around:{radius_m},{lat},{lon})["harbour"];
#       way(around:{radius_m},{lat},{lon})["harbour"];
#       node(around:{radius_m},{lat},{lon})["man_made"="pier"];
#       way(around:{radius_m},{lat},{lon})["man_made"="pier"];

#       node(around:{radius_m},{lat},{lon})["industrial"];
#       way(around:{radius_m},{lat},{lon})["industrial"];
#       node(around:{radius_m},{lat},{lon})["man_made"="works"];
#       way(around:{radius_m},{lat},{lon})["man_made"="works"];

#       node(around:{radius_m},{lat},{lon})["tourism"="hotel"];
#       way(around:{radius_m},{lat},{lon})["tourism"="hotel"];
#       node(around:{radius_m},{lat},{lon})["tourism"="guest_house"];
#       way(around:{radius_m},{lat},{lon})["tourism"="guest_house"];
#       node(around:{radius_m},{lat},{lon})["tourism"="resort"];
#       way(around:{radius_m},{lat},{lon})["tourism"="resort"];
#     );
#     out tags center;
#     """
#     resp = requests.get(OVERPASS_URL, params={"data": query}, timeout=timeout+10)
#     resp.raise_for_status()
#     return resp.json()

# def fetch_osm_counts(lat: float, lon: float, radius_m: int = 5000, pause_s: float = 1.5):
#     key = make_key("osm", lat=lat, lon=lon, radius_m=radius_m)
#     cached = cache_get(key)
#     if cached is not None:
#         return cached

#     try:
#         data = _overpass_query_for_point(lat, lon, radius_m=radius_m)
#     except Exception as e:
#         print("Overpass request failed:", e)
#         return None

#     count_ports = 0
#     count_industries = 0
#     count_hotels = 0
#     for el in data.get("elements", []):
#         tags = el.get("tags", {}) or {}
#         if tags.get("harbour") is not None or tags.get("man_made") == "pier":
#             count_ports += 1
#             continue
#         if tags.get("industrial") is not None or tags.get("man_made") == "works":
#             count_industries += 1
#             continue
#         if tags.get("tourism") in {"hotel", "guest_house", "resort"}:
#             count_hotels += 1
#             continue

#     obj = {
#         "lat": lat,
#         "lon": lon,
#         "count_ports": count_ports,
#         "count_industries": count_industries,
#         "count_hotels": count_hotels
#     }
#     cache_set(key, obj)
#     time.sleep(pause_s)
#     return obj

# def fetch_grid(coords: List[Tuple[float,float]], radius_m=5000, pause_s=1.5):
#     out = []
#     for lat, lon in coords:
#         c = fetch_osm_counts(lat, lon, radius_m=radius_m, pause_s=pause_s)
#         if c:
#             out.append(c)
#     return out

# if __name__ == "__main__":
#     from utils import grid_from_bbox
#     pts = grid_from_bbox(8.0, 72.0, 22.6, 88.4, step_m=25000)
#     import pandas as pd
#     rows = fetch_grid(pts[:20])
#     df = pd.DataFrame(rows)
#     df.to_csv("data/osm_samples.csv", index=False)
#     print("Saved data/osm_samples.csv")































# fetch_osm.py (drop-in replacement)
import requests, time, random
from utils import cache_get, cache_set, make_key

# Multiple Overpass mirrors for reliability
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter"
]

def _query(lat, lon, radius_m=5000, timeout=60):
    query = f"""[out:json][timeout:{timeout}];
    (
      node(around:{radius_m},{lat},{lon})["harbour"];
      node(around:{radius_m},{lat},{lon})["industrial"];
      node(around:{radius_m},{lat},{lon})["man_made"="works"];
      node(around:{radius_m},{lat},{lon})["tourism"~"hotel|guest_house|resort"];
    ); out tags;"""
    
    for attempt in range(5):
        url = random.choice(OVERPASS_URLS)
        try:
            r = requests.get(url, params={"data": query}, timeout=timeout + 10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"⚠️ Overpass error ({url}): {e}")
            time.sleep(5 * (attempt + 1))  # progressive back-off
    return {"elements": []}

def fetch_osm_counts(lat, lon, radius_m=5000, pause_s=2.5):
    key = make_key("osm", lat=lat, lon=lon, radius_m=radius_m)
    cached = cache_get(key)
    if cached:
        return cached

    data = _query(lat, lon, radius_m)
    ports = industries = hotels = 0
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        if "harbour" in tags:
            ports += 1
        elif "industrial" in tags or tags.get("man_made") == "works":
            industries += 1
        elif tags.get("tourism") in {"hotel", "guest_house", "resort"}:
            hotels += 1

    result = {"lat": lat, "lon": lon,
              "count_ports": ports,
              "count_industries": industries,
              "count_hotels": hotels}
    cache_set(key, result)
    time.sleep(pause_s)
    return result
