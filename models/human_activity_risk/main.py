# import numpy as np
# import pandas as pd
# from tqdm import tqdm

# from data_fetchers.ships import get_ship_density
# from data_fetchers.industries import count_industries
# from data_fetchers.hotels import count_hotels
# from data_fetchers.ports import count_near_ports
# from risk_model import train_model, load_model
# from utils.heatmap import create_map
# from utils.recommendations import risk_badge, recommendation

# def generate_dataset(lat_min=8.0, lat_max=22.0, lon_min=72.0, lon_max=88.0, step=2.0):
#     """
#     Build grid across bounding box and fetch features for each point.
#     Returns dataframe with columns: lat, lon, ports, industries, hotels, ships, activity_score
#     """
#     grid = [
#         (round(lat, 6), round(lon, 6))
#         for lat in np.arange(lat_min, lat_max, step)
#         for lon in np.arange(lon_min, lon_max, step)
#     ]
#     rows = []
#     print(f"🗺️ Generating grid of {len(grid)} points...")
#     for lat, lon in tqdm(grid, desc="Fetching grid data"):
#         ports_count = count_near_ports(lat, lon)
#         inds = count_industries(lat, lon)
#         hotels_count = count_hotels(lat, lon)
#         ships_count = get_ship_density(lat, lon)
#         # activity_score formula (weights can be tuned later)
#         activity_score = ports_count*2 + inds*3 + hotels_count*1 + ships_count*4
#         rows.append([lat, lon, ports_count, inds, hotels_count, ships_count, activity_score])

#     df = pd.DataFrame(rows, columns=["lat", "lon", "ports", "industries", "hotels", "ships", "activity_score"])
#     df.to_csv("activity_dataset.csv", index=False)
#     print("✅ Saved activity_dataset.csv")
#     return df

# def example_query(model, lat=19.07, lon=72.87):
#     ports_count = count_near_ports(lat, lon)
#     inds = count_industries(lat, lon)
#     hotels_count = count_hotels(lat, lon)
#     ships_count = get_ship_density(lat, lon)
#     X = pd.DataFrame([[ports_count, inds, hotels_count, ships_count]], columns=["ports","industries","hotels","ships"])
#     score = model.predict(X)[0]
#     print("\n📍 Example location:", lat, lon)
#     print("activity_risk →", round(score,2))
#     print("risk badge →", risk_badge(score))
#     print("recommendation →", recommendation(score))

# if __name__ == "__main__":
#     df = generate_dataset(step=2.0)   # change step smaller to increase resolution
#     model = train_model(df)
#     create_map(df, output="activity_map.html")
    # example_query(model)





# import numpy as np
# import pandas as pd
# from tqdm import tqdm

# from data_fetchers.ships import get_ship_density
# from data_fetchers.industries import count_industries
# from data_fetchers.hotels import count_hotels
# from data_fetchers.ports import count_near_ports
# from risk_model import train_model, load_model
# from utils.heatmap import create_map
# from utils.recommendations import risk_badge, recommendation

# FEATURE_COLS = ["ports", "industries", "hotels", "ships"]

# def generate_dataset(lat_min=8.0, lat_max=22.0, lon_min=72.0, lon_max=88.0, step=2.0):
#     """
#     Build grid across bounding box and fetch features for each point.
#     Returns dataframe with columns: lat, lon, ports, industries, hotels, ships, activity_score_target
#     """
#     grid = [
#         (round(lat, 6), round(lon, 6))
#         for lat in np.arange(lat_min, lat_max, step)
#         for lon in np.arange(lon_min, lon_max, step)
#     ]
#     rows = []
#     print(f"🗺️ Generating grid of {len(grid)} points...")
#     for lat, lon in tqdm(grid, desc="Fetching grid data"):
#         ports_count = count_near_ports(lat, lon)
#         inds = count_industries(lat, lon)
#         hotels_count = count_hotels(lat, lon)
#         ships_count = get_ship_density(lat, lon)

#         rows.append([lat, lon, ports_count, inds, hotels_count, ships_count])

#     df = pd.DataFrame(rows, columns=["lat", "lon", "ports", "industries", "hotels", "ships"])

#     # ----------------------------
#     # Create normalized features and a stable weighted target (0-100)
#     # ----------------------------
#     # MinMax normalization per-feature (we will persist scaler in risk_model)
#     # Build the weighted target (teacher) so RF can learn it.
#     # Keep the same weights used earlier for compatibility.
#     df_norm = df.copy()
#     for col in FEATURE_COLS:
#         col_min = df_norm[col].min()
#         col_max = df_norm[col].max()
#         # avoid division by zero
#         df_norm[col] = (df_norm[col] - col_min) / (col_max - col_min + 1e-9)

#     df_norm["activity_score"] = (
#         df_norm["ports"] * 0.25 +
#         df_norm["industries"] * 0.35 +
#         df_norm["hotels"] * 0.15 +
#         df_norm["ships"] * 0.60
#     ) * 100.0

#     # attach normalized columns and target back to df (keep original lat/lon)
#     for col in FEATURE_COLS:
#         df[col] = df_norm[col]
#     df["activity_score"] = df_norm["activity_score"]

#     df.to_csv("activity_dataset.csv", index=False)
#     print("✅ Saved activity_dataset.csv")
#     return df


# def example_query(model, scaler, df_reference, lat=19.07, lon=72.87):
#     # fetch raw counts
#     ports_count = count_near_ports(lat, lon)
#     inds = count_industries(lat, lon)
#     hotels_count = count_hotels(lat, lon)
#     ships_count = get_ship_density(lat, lon)

#     # build feature vector and scale using provided scaler
#     raw = np.array([[ports_count, inds, hotels_count, ships_count]], dtype=float)
#     X_scaled = scaler.transform(raw)  # scaler fitted inside train_model
#     score = model.predict(X_scaled)[0]

#     print("\n📍 Example location:", lat, lon)
#     print("activity_risk →", round(float(score), 2))
#     print("risk badge →", risk_badge(float(score)))
#     print("recommendation →", recommendation(float(score)))


# if __name__ == "__main__":
#     # generate dataset (1° grid recommended earlier; current default step=2.0)
#     df = generate_dataset(step=2.0)

#     # train_model returns (model, scaler)
#     model, scaler = train_model(df)

#     # create map using normalized activity_score in df
#     create_map(df, output="activity_map.html")

#     # example query uses model + scaler + df (df only used for metadata if necessary)
#     example_query(model, scaler, df)
































# import numpy as np
# import pandas as pd
# from tqdm import tqdm
# import argparse

# from data_fetchers.ships import get_ship_density
# from data_fetchers.industries import count_industries
# from data_fetchers.hotels import count_hotels
# from data_fetchers.ports import count_near_ports
# from risk_model import train_model, load_model
# from utils.heatmap import create_map
# from utils.recommendations import risk_badge, recommendation

# FEATURE_COLS = ["ports", "industries", "hotels", "ships"]


# def generate_dataset(lat_min=8.0, lat_max=22.0, lon_min=72.0, lon_max=88.0, step=2.0):
#     grid = [
#         (round(lat, 6), round(lon, 6))
#         for lat in np.arange(lat_min, lat_max, step)
#         for lon in np.arange(lon_min, lon_max, step)
#     ]
#     rows = []
#     print(f"🗺️ Generating grid of {len(grid)} points...")

#     for lat, lon in tqdm(grid, desc="Fetching grid data"):
#         ports_count = count_near_ports(lat, lon)
#         inds = count_industries(lat, lon)
#         hotels_count = count_hotels(lat, lon)
#         ships_count = get_ship_density(lat, lon)

#         rows.append([lat, lon, ports_count, inds, hotels_count, ships_count])

#     df = pd.DataFrame(rows, columns=["lat", "lon", "ports", "industries", "hotels", "ships"])

#     # ---------- Normalize and compute activity_score ----------
#     df_norm = df.copy()

#     for col in FEATURE_COLS:
#         col_min = df_norm[col].min()
#         col_max = df_norm[col].max()
#         df_norm[col] = (df_norm[col] - col_min) / (col_max - col_min + 1e-9)

#     df_norm["activity_score"] = (
#         df_norm["ports"] * 0.25 +
#         df_norm["industries"] * 0.35 +
#         df_norm["hotels"] * 0.15 +
#         df_norm["ships"] * 0.60
#     ) * 100.0

#     for col in FEATURE_COLS:
#         df[col] = df_norm[col]
#     df["activity_score"] = df_norm["activity_score"]

#     df.to_csv("activity_dataset.csv", index=False)
#     print("✅ Saved activity_dataset.csv")
#     return df


# def predict_from_cli(model, scaler, lat, lon):
#     ports_count = count_near_ports(lat, lon)
#     inds = count_industries(lat, lon)
#     hotels_count = count_hotels(lat, lon)
#     ships_count = get_ship_density(lat, lon)

#     raw = np.array([[ports_count, inds, hotels_count, ships_count]], dtype=float)
#     X_scaled = scaler.transform(raw)

#     score = float(model.predict(X_scaled)[0])

#     print("\n📍 Location:", lat, lon)
#     print("ports:", ports_count, "| industries:", inds, "| hotels:", hotels_count, "| ships:", ships_count)
#     print("activity_risk →", round(score, 2))
#     print("risk badge →", risk_badge(score))
#     print("recommendation →", recommendation(score))


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--lat", type=float, help="Latitude for prediction")
#     parser.add_argument("--lon", type=float, help="Longitude for prediction")
#     args = parser.parse_args()

#     df = generate_dataset(step=2.0)

#     model, scaler = train_model(df)

#     create_map(df, output="activity_map.html")

#     if args.lat is not None and args.lon is not None:
#         predict_from_cli(model, scaler, args.lat, args.lon)
#     else:
#         print("\nℹ️ No lat/lon provided. Using default: Mumbai (19.0760, 72.8777)")
#         predict_from_cli(model, scaler, 19.0760, 72.8777)















import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils.heatmap import create_map


from data_fetchers.ships import get_ship_density
from data_fetchers.industries import count_industries
from data_fetchers.hotels import count_hotels
from data_fetchers.ports import count_near_ports
from risk_model import train_model, load_model, load_scaler
from utils.heatmap import create_map
from utils.recommendations import risk_badge, recommendation
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')


FEATURE_COLS = ["ports", "industries", "hotels", "ships"]


def predict_location(model, scaler, lat, lon):
    ports = count_near_ports(lat, lon)
    inds = count_industries(lat, lon)
    hotels = count_hotels(lat, lon)
    ships = get_ship_density(lat, lon)

    raw = np.array([[ports, inds, hotels, ships]])
    scaled = scaler.transform(raw)
    score = float(model.predict(scaled)[0])

    rec = recommendation(score).replace("\n", " | ")

    print(f"\n📍 Location: {lat} {lon}")
    print(f"ports: {ports} | industries: {inds} | hotels: {hotels} | ships: {ships}")
    print("activity_risk →", round(score, 2))
    print("risk badge →", risk_badge(score))
    print("recommendation →", recommendation(score))
    # 🔥 Generate heatmap file
    create_map(args.lat, args.lon, score)
    print("🔥 Heatmap generated for frontend")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    args = parser.parse_args()

    df = pd.read_csv("activity_dataset.csv")
    model = load_model()
    scaler = load_scaler()

    # ⭐ ADDED FOR HEATMAP — regenerate heatmap every RUN
    create_map(df, output="../../frontend/public/heatmaps/activity_map.html")

    # ---- Prediction ----
    predict_location(model, scaler, args.lat, args.lon)

    # ---- 🔥 Generate Heatmap ----
    print("\n🔥 Generating Heatmap…")
    create_map(args.lat, args.lon, float(model.predict(
        scaler.transform([[ 
            count_near_ports(args.lat, args.lon),
            count_industries(args.lat, args.lon),
            count_hotels(args.lat, args.lon),
            get_ship_density(args.lat, args.lon)
        ]])
    )[0]))
    print("🔥 Heatmap generated successfully!")
