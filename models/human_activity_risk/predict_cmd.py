# # predict_cmd.py
# import click
# import joblib
# import numpy as np
# import os
# from fetch_osm import fetch_osm_counts
# from utils import compute_activity_score_array
# from fetch_satellite import get_satellite_label

# MODEL_PATH = "models/best_pipeline.joblib"

# @click.command()
# @click.option("--lat", type=float, required=True)
# @click.option("--lon", type=float, required=True)
# @click.option("--radius", type=int, default=5000)
# @click.option("--date", type=str, default=None, help="Date (YYYY-MM-DD) for satellite label (optional)")
# def main(lat, lon, radius, date):
#     if not os.path.exists(MODEL_PATH):
#         print("Model not found — run train_model.py first")
#         return
#     pipeline = joblib.load(MODEL_PATH)
#     counts = fetch_osm_counts(lat, lon, radius_m=radius)
#     if counts is None:
#         print("OSM fetch failed.")
#         return
#     activity = compute_activity_score_array([counts["count_ports"]], [counts["count_industries"]], [counts["count_hotels"]])[0]
#     X = np.array([[counts["count_ports"], counts["count_industries"], counts["count_hotels"], activity]])
#     pred_raw = pipeline.predict(X)[0]
#     print(f"Predicted pollutant value (e.g., NO₂ column) = {pred_raw:.6f}")
#     # Map “pred_raw” to 0-100 risk scale
#     # Define bounds for NO₂ column (for your region): e.g., low=0 µmol/m², high=0.0002 µmol/m²
#     low, high = 0.0, 0.0002
#     risk_pct = 100.0 * (np.clip(pred_raw, low, high) - low) / (high - low)
#     print(f"Mapped activity_risk (0-100): {risk_pct:.2f}")
#     # show cached satellite label
#     sat_val = get_satellite_label(lat, lon, date=date, radius_km=radius/1000)
#     print("Actual satellite label (if fetched/cached):", sat_val)

# if __name__ == "__main__":
#     main()
























# predict_cmd.py
import click, joblib, numpy as np, os
from fetch_osm import fetch_osm_counts
from utils import compute_activity_score_array

@click.command()
@click.option("--lat",type=float,required=True)
@click.option("--lon",type=float,required=True)
@click.option("--radius",default=5000,type=int)
def main(lat,lon,radius):
    if not os.path.exists("models/best_pipeline.joblib"):
        print("Train first.");return
    model=joblib.load("models/best_pipeline.joblib")
    counts=fetch_osm_counts(lat,lon,radius_m=radius)
    if not counts:print("OSM fail");return
    activity=compute_activity_score_array([counts["count_ports"]],[counts["count_industries"]],[counts["count_hotels"]])[0]
    X=np.array([[counts["count_ports"],counts["count_industries"],counts["count_hotels"],activity]])
    pred=model.predict(X)[0]
    low,high=float(np.nanmin([0,pred*0.5])),float(np.nanmax([pred*2,1e-5]))
    risk=100*(pred-low)/(high-low)
    print(f"Predicted pollutant≈{pred:.5f} | Risk={risk:.1f}/100")

if __name__=="__main__":
    main()
