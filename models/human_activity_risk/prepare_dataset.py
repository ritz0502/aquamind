# # prepare_dataset.py
# import pandas as pd
# import numpy as np
# import os
# from fetch_osm import fetch_grid, fetch_osm_counts
# from fetch_satellite import get_satellite_label
# from utils import compute_activity_score_array, grid_from_bbox

# DATA_CSV = "data/osm_samples_joined.csv"
# HEATMAP_CSV = "outputs/heatmap_ready.csv"

# def prepare_from_bbox(min_lat, min_lon, max_lat, max_lon, grid_step_m=5000, radius=5000, product_files=None, pause_s=1.5):
#     os.makedirs("data", exist_ok=True)
#     os.makedirs("outputs", exist_ok=True)
#     pts = grid_from_bbox(min_lat, min_lon, max_lat, max_lon, step_m=grid_step_m)
#     print(f"Generated {len(pts)} grid points")

#     rows = []
#     for i, (lat, lon) in enumerate(pts):
#         print(f"[{i+1}/{len(pts)}] fetching OSM {lat:.5f},{lon:.5f}")
#         counts = fetch_osm_counts(lat, lon, radius_m=radius, pause_s=pause_s)
#         if counts is None:
#             print(" -> OSM fetch failed")
#             continue

#         sat_val = get_satellite_label(lat, lon, date=None, radius_km=radius/1000, product_files=product_files)
#         row = counts.copy()
#         row["sat_label"] = sat_val
#         rows.append(row)

#     if not rows:
#         raise RuntimeError("No data rows collected.")

#     df = pd.DataFrame(rows)
#     df["activity_score"] = compute_activity_score_array(df["count_ports"], df["count_industries"], df["count_hotels"])
#     df_valid = df.dropna(subset=["sat_label"]).reset_index(drop=True)
#     print(f"Collected {len(df)} rows; {len(df_valid)} rows with valid satellite label")

#     df_valid.to_csv(DATA_CSV, index=False)
#     df_heat = df.copy()
#     df_heat["risk_probe"] = df_heat["sat_label"].fillna(df_heat["activity_score"]*100)
#     df_heat[["lat", "lon", "risk_probe"]].to_csv(HEATMAP_CSV, index=False)
#     print("Saved:", DATA_CSV, HEATMAP_CSV)
#     return df_valid

# if __name__ == "__main__":
#     # Example region (adjust to your coastline segment)
#     df = prepare_from_bbox(8.0, 72.0, 22.6, 88.4, grid_step_m=50000, radius=5000, product_files=None, pause_s=2)
#     print(df.head())



























# # prepare_dataset.py
# import pandas as pd
# import numpy as np
# import os
# from tqdm import tqdm
# from utils import compute_activity_score_array, grid_from_bbox
# from fetch_osm import fetch_osm_counts
# from fetch_satellite import fetch_many_points

# DATA_CSV = "data/osm_samples_joined.csv"
# HEATMAP_CSV = "outputs/heatmap_ready.csv"

# def prepare_from_bbox(min_lat, min_lon, max_lat, max_lon,
#                       grid_step_m=50000, radius=5000,
#                       variable="chlor_a"):
#     os.makedirs("data", exist_ok=True)
#     os.makedirs("outputs", exist_ok=True)

#     # Generate grid points
#     pts = grid_from_bbox(min_lat, min_lon, max_lat, max_lon,
#                          step_m=grid_step_m)
#     print(f"🗺️  Generated {len(pts)} grid points")

#     # Step 1: Fetch OSM data
#     osm_rows = []
#     for lat, lon in tqdm(pts, desc="Fetching OSM"):
#         counts = fetch_osm_counts(lat, lon, radius_m=radius)
#         if counts:
#             osm_rows.append(counts)
#     df_osm = pd.DataFrame(osm_rows)

#     # Step 2: Fetch Copernicus data (parallel)
#     print("\n🌊 Fetching Copernicus Marine data (parallel)...")
#     cmems_data = fetch_many_points(variable, pts,
#                                    start_date="2025-10-10",
#                                    end_date="2025-11-09")

#     # Step 3: Join data
#     sat_vals = []
#     for lat, lon in pts:
#         df_var = cmems_data.get((lat, lon))
#         val = np.nan
#         if isinstance(df_var, pd.DataFrame) and not df_var.empty:
#             try:
#                 df_var[variable] = pd.to_numeric(df_var[variable],
#                                                  errors="coerce")
#                 val = float(df_var[variable].mean(skipna=True))
#             except Exception:
#                 pass
#         sat_vals.append(val)

#     df_osm["sat_label"] = sat_vals

#     # Step 4: Compute activity score
#     df_osm["activity_score"] = compute_activity_score_array(
#         df_osm["count_ports"], df_osm["count_industries"],
#         df_osm["count_hotels"]
#     )

#     # Step 5: Save outputs
#     df_valid = df_osm.dropna(subset=["sat_label"])
#     df_valid.to_csv(DATA_CSV, index=False)
#     df_osm.assign(risk_probe=df_osm["activity_score"] * 100)[
#         ["lat", "lon", "risk_probe"]
#     ].to_csv(HEATMAP_CSV, index=False)

#     print(f"✅ Saved {DATA_CSV} ({len(df_valid)} valid rows)")
#     return df_valid


# if __name__ == "__main__":
#     prepare_from_bbox(8.0, 72.0, 22.6, 88.4)




























# prepare_dataset.py
from fetch_osm_local import fetch_osm_counts
import pandas as pd
import numpy as np
from tqdm import tqdm
import os

def generate_grid(lat_min, lon_min, lat_max, lon_max, step_km=50):
    step_deg = step_km / 111
    lats = np.arange(lat_min, lat_max, step_deg)
    lons = np.arange(lon_min, lon_max, step_deg)
    return [(lat, lon) for lat in lats for lon in lons]

def prepare_from_bbox(lat_min, lon_min, lat_max, lon_max, radius_m=5000):
    grid = generate_grid(lat_min, lon_min, lat_max, lon_max)
    print(f"🗺️  Generated {len(grid)} grid points")

    data = []
    for i, (lat, lon) in enumerate(tqdm(grid, desc="Fetching OSM")):
        counts = fetch_osm_counts(lat, lon, radius_m)
        data.append(counts)

    df = pd.DataFrame(data)
    df["activity_score"] = (df["count_ports"]*2 + df["count_industries"]*3 + df["count_hotels"]*1)
    df["activity_score"] = (df["activity_score"] - df["activity_score"].min()) / \
                           (df["activity_score"].max() - df["activity_score"].min()) * 100

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/activity_dataset.csv", index=False)
    print("✅ Dataset saved to data/activity_dataset.csv")
    return df

if __name__ == "__main__":
    prepare_from_bbox(8.0, 72.0, 22.6, 88.4)
