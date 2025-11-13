# # generate_synthetic_data.py
# """
# Generate medium-size synthetic datasets that mirror real AIS/VIIRS/POI behavior
# for the India coastal bbox (lat 8.0-22.6, lon 72.0-88.4).

# Outputs (into ./data/):
#  - synthetic_ships.csv       (lat,lon,ships)
#  - synthetic_industries.csv  (lat,lon,industry_count)
#  - synthetic_hotels.csv      (lat,lon,hotel_count)
#  - synthetic_nightlights.csv (lat,lon,radiance)
# """
# import os
# import math
# import random
# import csv
# import numpy as np

# OUT_DIR = "data"
# os.makedirs(OUT_DIR, exist_ok=True)

# # bounding box
# LAT_MIN, LAT_MAX = 8.0, 22.6
# LON_MIN, LON_MAX = 72.0, 88.4

# # grid (medium ~400 points)
# NX = 20
# NY = 20
# lats = np.linspace(LAT_MIN, LAT_MAX, NX)
# lons = np.linspace(LON_MIN, LON_MAX, NY)
# grid = [(float(round(lat,6)), float(round(lon,6))) for lat in lats for lon in lons]

# # hotspots roughly at major ports/cities (lat, lon, relative strength)
# HOTSPOTS = [
#     (19.07, 72.87, 1.0),   # Mumbai
#     (13.08, 80.27, 0.8),   # Chennai
#     (22.57, 88.36, 0.7),   # Kolkata
#     (9.97, 76.28, 0.6),    # Kochi
#     (17.68, 83.21, 0.5),   # Visakhapatnam
#     (15.50, 73.80, 0.6),   # Goa
#     (10.80, 79.14, 0.35),  # Puducherry-ish
# ]

# def haversine_km(a_lat, a_lon, b_lat, b_lon):
#     # returns km distance
#     R = 6371.0
#     a_lat_r, a_lon_r = math.radians(a_lat), math.radians(a_lon)
#     b_lat_r, b_lon_r = math.radians(b_lat), math.radians(b_lon)
#     dlat = b_lat_r - a_lat_r
#     dlon = b_lon_r - a_lon_r
#     aa = math.sin(dlat/2)**2 + math.cos(a_lat_r)*math.cos(b_lat_r)*math.sin(dlon/2)**2
#     return 2*R*math.asin(math.sqrt(aa))

# def gaussian_influence(lat, lon, center_lat, center_lon, sigma_km=100):
#     d = haversine_km(lat, lon, center_lat, center_lon)
#     return math.exp(-0.5*(d/sigma_km)**2)

# # build base ship density (continuous)
# ships = []
# industries = []
# hotels = []
# nightlights = []

# for (lat, lon) in grid:
#     # base random sea/coast bias: points closer to coast hotspots get higher base
#     base = 0.05  # minimum background
#     # sum contributions from hotspots
#     ship_mu = base * 5.0  # baseline mean ships
#     ind_mu = 0.1
#     hotel_mu = 0.1
#     night_mu = 0.5

#     for (h_lat, h_lon, strength) in HOTSPOTS:
#         influence = gaussian_influence(lat, lon, h_lat, h_lon, sigma_km=120)  # 120km spread
#         ship_mu += influence * (30.0 * strength)
#         ind_mu += influence * (6.0 * strength)
#         hotel_mu += influence * (8.0 * strength)
#         night_mu += influence * (50.0 * strength)

#     # add a coastline band effect: more ships near lat/lon edges facing sea
#     # simple trick: if lon between 72-76 or 84-88 (west/east sea edge), increase ships
#     if lon < 76.5 or lon > 85.0:
#         ship_mu *= 1.25

#     # sample counts (poisson-ish but allow decimal)
#     ships_count = np.random.poisson(max(0.2, ship_mu))
#     industry_count = np.random.poisson(max(0.0, ind_mu))
#     hotel_count = np.random.poisson(max(0.0, hotel_mu))
#     # radiance: continuous positive with noise (higher near hotspots)
#     radiance = max(0.0, np.random.normal(loc=night_mu, scale=night_mu*0.3))

#     ships.append((lat, lon, int(ships_count)))
#     industries.append((lat, lon, int(industry_count)))
#     hotels.append((lat, lon, int(hotel_count)))
#     nightlights.append((lat, lon, float(round(radiance,3))))

# # add a few random industrial super-clusters (simulate big industrial zones)
# extra_inds = [
#     (21.5, 88.0, 120),  # big port cluster near kolkata
#     (20.0, 72.6, 90),   # near mumbai/gulf
#     (13.0, 80.2, 70),   # chennai industry
# ]
# for (clat, clon, cval) in extra_inds:
#     # find nearest grid point and add
#     dmin = 1e9; idx = None
#     for i,(lat,lon,_) in enumerate(industries):
#         d = haversine_km(lat, lon, clat, clon)
#         if d < dmin:
#             dmin = d; idx = i
#     if idx is not None:
#         lat,lon,old = industries[idx]
#         industries[idx] = (lat, lon, int(old + cval))

# # save CSVs
# def write_csv(path, header, rows):
#     with open(path, "w", newline="") as f:
#         w = csv.writer(f)
#         w.writerow(header)
#         for r in rows:
#             w.writerow(r)

# write_csv(os.path.join(OUT_DIR, "synthetic_ships.csv"), ["lat","lon","ships"], ships)
# write_csv(os.path.join(OUT_DIR, "synthetic_industries.csv"), ["lat","lon","industry_count"], industries)
# write_csv(os.path.join(OUT_DIR, "synthetic_hotels.csv"), ["lat","lon","hotel_count"], hotels)
# write_csv(os.path.join(OUT_DIR, "synthetic_nightlights.csv"), ["lat","lon","radiance"], nightlights)

# print("Generated synthetic CSVs in", OUT_DIR)
# print("Points:", len(grid))









































# # generate_synthetic_data.py
# """
# Ultra-accuracy synthetic data generator (Option 2).
# Creates dense, realistic synthetic points for India bbox:
# lat 8.0 - 22.0, lon 72.0 - 88.0

# Outputs to ./data/:
#  - synthetic_ships.csv       (lat,lon,ships)   ships=1 per row
#  - synthetic_industries.csv  (lat,lon,industry_count) industry_count=1 per row
#  - synthetic_hotels.csv      (lat,lon,hotel_count) hotel_count=1 per row
#  - synthetic_ports.csv       (lat,lon,ports) ports=1 per row

# Run: python generate_synthetic_data.py
# """
# import os, csv, math, random
# import numpy as np

# OUT = "data"
# os.makedirs(OUT, exist_ok=True)

# LAT_MIN, LAT_MAX = 8.0, 22.0
# LON_MIN, LON_MAX = 72.0, 88.0

# # Hotspot centers (lat, lon, relative weight)
# HOTSPOTS = [
#     (19.07, 72.87, 1.00),   # Mumbai
#     (13.08, 80.27, 0.9),    # Chennai
#     (22.57, 88.36, 0.9),    # Kolkata
#     (9.97, 76.28, 0.7),     # Kochi
#     (17.68, 83.21, 0.6),    # Visakhapatnam
#     (15.50, 73.80, 0.6),    # Goa
#     (11.0, 92.5, 0.2)       # Andaman-ish small
# ]

# def sample_clusters(n, base_spread_km=60):
#     """Sample n points around hotspots + random coastal/inland."""
#     pts = []
#     # allocate most points to hotspots with some coastal + inland noise
#     for i in range(n):
#         r = random.random()
#         if r < 0.7:
#             # hotspot sample
#             center = random.choices(HOTSPOTS, weights=[h[2] for h in HOTSPOTS])[0]
#             lat0, lon0 = center[0], center[1]
#             # sample gaussian in degrees approx (1 deg ~ 111 km)
#             sigma_deg = base_spread_km / 111.0
#             lat = np.clip(np.random.normal(lat0, sigma_deg), LAT_MIN, LAT_MAX)
#             lon = np.clip(np.random.normal(lon0, sigma_deg), LON_MIN, LON_MAX)
#         elif r < 0.9:
#             # coastal belt sampling (random lon near coastline edges)
#             lat = random.uniform(LAT_MIN, LAT_MAX)
#             if random.random() < 0.6:
#                 # west coast bias
#                 lon = random.uniform(72.0, 76.5)
#             else:
#                 lon = random.uniform(84.5, 88.0)
#         else:
#             # inland low-density
#             lat = random.uniform(LAT_MIN, LAT_MAX)
#             lon = random.uniform(74.0, 86.0)
#         pts.append((round(float(lat),6), round(float(lon),6)))
#     return pts

# def write_pairs(path, header, pairs):
#     with open(path, "w", newline="") as f:
#         w = csv.writer(f)
#         w.writerow(header)
#         for (lat, lon) in pairs:
#             w.writerow([lat, lon, 1])  # count = 1 per record

# # Option 2 counts (Ultra Accuracy)
# N_SHIPS = 8000
# N_INDS = 8000
# N_HOTELS = 8000
# N_PORTS = 1500

# print("Generating synthetic ships ...")
# ships_pts = sample_clusters(N_SHIPS, base_spread_km=40)
# write_pairs(os.path.join(OUT, "synthetic_ships.csv"), ["lat","lon","ships"], ships_pts)

# print("Generating synthetic industries ...")
# inds_pts = sample_clusters(N_INDS, base_spread_km=30)
# write_pairs(os.path.join(OUT, "synthetic_industries.csv"), ["lat","lon","industry_count"], inds_pts)

# print("Generating synthetic hotels ...")
# hotels_pts = sample_clusters(N_HOTELS, base_spread_km=20)
# write_pairs(os.path.join(OUT, "synthetic_hotels.csv"), ["lat","lon","hotel_count"], hotels_pts)

# print("Generating synthetic ports ...")
# # ports concentrated more strictly on coast hotspots; make them tighter
# ports_pts = sample_clusters(N_PORTS, base_spread_km=12)
# write_pairs(os.path.join(OUT, "synthetic_ports.csv"), ["lat","lon","ports"], ports_pts)

# print("Done. Files written to 'data/'")
# print("Counts:", len(ships_pts), len(inds_pts), len(hotels_pts), len(ports_pts))




























# # generate_synthetic_data.py
# """
# Improved synthetic generator (Option 2, aggregated counts).

# Generates aggregated counts per spatial bin so CSVs contain realistic counts,
# not just rows with '1'.

# Outputs to ./data/:
#  - synthetic_ships.csv       (lat,lon,ships)       counts aggregated per bin
#  - synthetic_industries.csv  (lat,lon,industry_count)
#  - synthetic_hotels.csv      (lat,lon,hotel_count)
#  - synthetic_ports.csv       (lat,lon,ports)

# Run:
#     python generate_synthetic_data.py
# """
# import os, csv, random, math
# from collections import defaultdict
# import numpy as np

# OUT = "data"
# os.makedirs(OUT, exist_ok=True)

# LAT_MIN, LAT_MAX = 8.0, 22.0
# LON_MIN, LON_MAX = 72.0, 88.0

# HOTSPOTS = [
#     (19.07, 72.87, 1.00),   # Mumbai
#     (13.08, 80.27, 0.95),   # Chennai
#     (22.57, 88.36, 0.9),    # Kolkata
#     (9.97, 76.28, 0.7),     # Kochi
#     (17.68, 83.21, 0.6),    # Visakhapatnam
#     (15.50, 73.80, 0.6),    # Goa
# ]

# def sample_point_around(center, sigma_deg):
#     lat0, lon0 = center
#     lat = np.random.normal(lat0, sigma_deg)
#     lon = np.random.normal(lon0, sigma_deg)
#     lat = float(max(min(lat, LAT_MAX), LAT_MIN))
#     lon = float(max(min(lon, LON_MAX), LON_MIN))
#     return round(lat, 6), round(lon, 6)

# def sample_clusters(n, base_spread_km=60, hotspot_frac=0.7):
#     pts = []
#     sigma_deg = base_spread_km / 111.0
#     for _ in range(n):
#         r = random.random()
#         if r < hotspot_frac:
#             center = random.choices([ (h[0],h[1]) for h in HOTSPOTS ],
#                                      weights=[h[2] for h in HOTSPOTS], k=1)[0]
#             pts.append(sample_point_around(center, sigma_deg))
#         elif r < hotspot_frac + 0.15:
#             # coastal strip
#             lat = random.uniform(LAT_MIN, LAT_MAX)
#             # bias to west or east coasts
#             if random.random() < 0.6:
#                 lon = random.uniform(72.0, 76.5)
#             else:
#                 lon = random.uniform(84.5, 88.0)
#             pts.append((round(lat,6), round(lon,6)))
#         else:
#             # inland low density
#             pts.append((round(random.uniform(LAT_MIN, LAT_MAX),6),
#                         round(random.uniform(74.0,86.0),6)))
#     return pts

# def aggregate_points(points, weight_sampler=None, round_dec=4):
#     """
#     points: list of (lat,lon)
#     weight_sampler: function() -> int weight for each sampled point (default 1)
#     round_dec: number of decimals to round lat/lon for binning
#     returns dict {(lat,lon): total_count}
#     """
#     agg = defaultdict(int)
#     for lat, lon in points:
#         latb = round(lat, round_dec)
#         lonb = round(lon, round_dec)
#         w = weight_sampler() if weight_sampler is not None else 1
#         agg[(latb, lonb)] += int(max(0, round(w)))
#     return agg

# def write_agg_csv(path, agg_dict, header_name):
#     with open(path, "w", newline="") as f:
#         w = csv.writer(f)
#         w.writerow(["lat","lon", header_name])
#         for (lat,lon),count in sorted(agg_dict.items(), key=lambda x: (-x[1], x[0])):
#             w.writerow([lat, lon, int(count)])

# # ---- Option 2 target sizes (Ultra Accuracy) ----
# N_SHIPS = 8000
# N_INDS = 8000
# N_HOTELS = 8000
# N_PORTS = 1500

# print("Sampling raw points... (this may take a few seconds)")

# ships_raw = sample_clusters(N_SHIPS, base_spread_km=40, hotspot_frac=0.75)
# inds_raw  = sample_clusters(N_INDS, base_spread_km=30, hotspot_frac=0.70)
# hotels_raw= sample_clusters(N_HOTELS, base_spread_km=20, hotspot_frac=0.80)
# ports_raw = sample_clusters(N_PORTS, base_spread_km=10, hotspot_frac=0.85)

# # Weight samplers: add realistic variability
# def ship_weight():
#     # ships per sampled point: 1-6 (simulate multiple vessels converging)
#     return max(1, int(np.random.poisson(1.2)))  # mostly 1 but some >1

# def industry_weight():
#     # industry cluster size: 1-10
#     return max(1, int(np.random.poisson(1.5)))

# def hotel_weight():
#     # hotels: can have multiple hotels at same bin
#     return max(1, int(np.random.poisson(1.8)))

# def port_weight():
#     # ports: small integer, but some bins aggregate to bigger ports
#     return max(1, int(np.random.poisson(2.0)))

# # Aggregate into spatial bins (round to 3-4 decimals)
# round_dec = 4  # bin size ~ 11m at equator × 10^-4 deg — fine-grained; adjust if too fine
# print("Aggregating ships...")
# agg_ships = aggregate_points(ships_raw, weight_sampler=ship_weight, round_dec=round_dec)
# print("Aggregating industries...")
# agg_inds  = aggregate_points(inds_raw,  weight_sampler=industry_weight, round_dec=round_dec)
# print("Aggregating hotels...")
# agg_hotels= aggregate_points(hotels_raw,weight_sampler=hotel_weight, round_dec=round_dec)
# print("Aggregating ports...")
# agg_ports = aggregate_points(ports_raw, weight_sampler=port_weight, round_dec=round_dec)

# # Optionally: smooth / bump some hotspot cells to simulate major ports
# def bump_cell(agg, lat, lon, extra):
#     key = (round(lat, round_dec), round(lon, round_dec))
#     agg[key] += extra

# # Bump known major ports/cities (approx coords)
# bump_cell(agg_ports, 19.07, 72.87, 40)   # Mumbai big port
# bump_cell(agg_ports, 13.08, 80.27, 30)   # Chennai
# bump_cell(agg_ports, 22.57, 88.36, 35)   # Kolkata
# bump_cell(agg_ships, 19.07, 72.87, 120)  # huge ship density off Mumbai
# bump_cell(agg_ships, 13.08, 80.27, 80)
# bump_cell(agg_inds, 20.2, 72.9, 200)     # industry cluster (Surat/Mumbai belt)
# bump_cell(agg_hotels, 15.5, 73.8, 80)    # Goa tourism

# # write CSVs (with aggregated counts)
# print("Writing CSVs...")
# write_agg_csv(os.path.join(OUT, "synthetic_ships.csv"), agg_ships, "ships")
# write_agg_csv(os.path.join(OUT, "synthetic_industries.csv"), agg_inds, "industry_count")
# write_agg_csv(os.path.join(OUT, "synthetic_hotels.csv"), agg_hotels, "hotel_count")
# write_agg_csv(os.path.join(OUT, "synthetic_ports.csv"), agg_ports, "ports")

# print("Done. Files written to data/:")
# print("  ships bins:", len(agg_ships))
# print("  industries bins:", len(agg_inds))
# print("  hotels bins:", len(agg_hotels))
# print("  ports bins:", len(agg_ports))




























# generate_synthetic_data.py
import numpy as np
import pandas as pd
import os
from utils.config import DATA_DIR

np.random.seed(42)

# ------------------------------------
# Define realistic hotspot clusters
# ------------------------------------
HOTSPOTS = {
    "ships": [
        (19.0, 72.8), (23.0, 70.0), (9.9, 76.2), (13.0, 80.2),
        (17.7, 83.3), (22.5, 88.3), (15.5, 73.8), (11.6, 92.7)
    ],
    "industries": [
        (22.8, 69.8), (19.1, 73.0), (12.9, 74.8),
        (13.0, 79.9), (20.3, 86.6), (17.7, 83.3), (22.0, 88.1)
    ],
    "hotels": [
        (15.5, 73.8), (9.5, 76.3), (11.6, 92.7),
        (11.9, 79.8), (19.0, 72.8), (13.0, 80.2), (17.7, 83.3)
    ],
    "ports": [
        (18.9, 72.9), (19.1, 72.95), (12.9, 74.8), (9.9, 76.2),
        (8.8, 78.1), (13.1, 80.3), (13.2, 80.3), (16.98, 82.27),
        (17.7, 83.3), (20.3, 86.6), (22.0, 88.1), (22.55, 88.28)
    ]
}

# How many points to generate
N = {
    "ships": 12000,
    "industries": 8000,
    "hotels": 10000,
    "ports": 2500
}

# Spread radius (degrees)
SPREAD = {
    "ships": 0.9,
    "industries": 0.5,
    "hotels": 0.7,
    "ports": 0.25
}

def sample_cluster(center, count, spread):
    lat0, lon0 = center
    lat = np.random.normal(lat0, spread, count)
    lon = np.random.normal(lon0, spread, count)
    return lat, lon

def generate_category(category, multiplier=1):
    points = []
    cat_hotspots = HOTSPOTS[category]
    total = N[category]
    spread = SPREAD[category]

    per_cluster = total // len(cat_hotspots)

    for center in cat_hotspots:
        lat, lon = sample_cluster(center, per_cluster, spread)
        for la, lo in zip(lat, lon):
            points.append([la, lo, np.random.randint(1, 20)])  # COUNT RANGE 1–20

    df = pd.DataFrame(points, columns=["lat", "lon", f"{category}_count"])
    df.to_csv(os.path.join(DATA_DIR, f"synthetic_{category}.csv"), index=False)
    return df

if __name__ == "__main__":
    print("Generating synthetic ships...")
    generate_category("ships")

    print("Generating synthetic industries...")
    generate_category("industries")

    print("Generating synthetic hotels...")
    generate_category("hotels")

    print("Generating synthetic ports...")
    generate_category("ports")

    print("\n✅ Synthetic datasets created inside /data/")
