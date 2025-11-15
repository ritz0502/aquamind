import argparse
import numpy as np
import pandas as pd

from data_fetchers.ships import get_ship_density
from data_fetchers.industries import count_industries
from data_fetchers.hotels import count_hotels
from data_fetchers.ports import count_near_ports

from risk_model import load_model, load_scaler
from utils.heatmap import create_map
from utils.recommendations import risk_badge, recommendation

import sys
sys.stdout.reconfigure(encoding='utf-8')


def predict_location(model, scaler, lat, lon):
    ports = count_near_ports(lat, lon)
    inds = count_industries(lat, lon)
    hotels = count_hotels(lat, lon)
    ships = get_ship_density(lat, lon)

    raw = np.array([[ports, inds, hotels, ships]])
    scaled = scaler.transform(raw)

    score = float(model.predict(scaled)[0])

    print(f"\n📍 Location: {lat} {lon}")
    print(f"ports: {ports} | industries: {inds} | hotels: {hotels} | ships: {ships}")
    print("activity_risk →", round(score, 2))
    print("risk badge →", risk_badge(score))
    print("recommendation →", recommendation(score))

    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    args = parser.parse_args()

    # Load trained model
    df = pd.read_csv("activity_dataset.csv")
    model = load_model()
    scaler = load_scaler()

    # ---- Predict ----
    score = predict_location(model, scaler, args.lat, args.lon)

    # ---- Generate Heatmap ----
    print("\n🔥 Generating Heatmap…")
    create_map(args.lat, args.lon, score)
    print("🔥 Heatmap generated successfully!")
