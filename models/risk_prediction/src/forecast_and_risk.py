import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import sys
sys.stdout.reconfigure(encoding='utf-8')


# === Directory Setup ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
OUTPUT_DIR = os.path.join(DATA_DIR, "risk")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


# === Load and Merge Forecasts ===
def load_forecast(variable, lat, lon):
    """Load Prophet (ds) and LSTM (time) forecasts and merge them."""
    prophet_path = os.path.join(FORECAST_DIR, f"forecast_prophet_{variable}_{lat}_{lon}.csv")
    lstm_path = os.path.join(FORECAST_DIR, f"forecast_lstm_{variable}_{lat}_{lon}.csv")

    # Prophet
    if not os.path.exists(prophet_path):
        print(f"⚠️ Skipping Prophet forecast — file not found for {variable}")
        prophet_df = pd.DataFrame(columns=["ds", "yhat"])
    else:
        prophet_df = pd.read_csv(prophet_path)

    # LSTM
    if not os.path.exists(lstm_path):
        print(f"⚠️ Skipping LSTM forecast — file not found for {variable}")
        lstm_df = pd.DataFrame(columns=["time", "forecast"])
    else:
        lstm_df = pd.read_csv(lstm_path)

    # Normalize Prophet columns
    if "ds" in prophet_df.columns:
        prophet_df.rename(columns={"ds": "time", "yhat": "prophet_forecast"}, inplace=True)

    # Normalize LSTM columns
    if "time" not in lstm_df.columns and "date" in lstm_df.columns:
        lstm_df.rename(columns={"date": "time"}, inplace=True)
    forecast_cols = [c for c in lstm_df.columns if "forecast" in c.lower()]
    if forecast_cols:
        lstm_df.rename(columns={forecast_cols[0]: "lstm_forecast"}, inplace=True)

    # Merge safely
    df = pd.merge(prophet_df[["time", "prophet_forecast"]],
                  lstm_df[["time", "lstm_forecast"]],
                  on="time", how="outer").sort_values("time")

    # Weighted ensemble
    df["ensemble_forecast"] = 0.6 * df.get("lstm_forecast", 0) + 0.4 * df.get("prophet_forecast", 0)
    return df[["time", "ensemble_forecast"]]



# === Risk Computation ===
def compute_risk_index(merged_df):
    """Compute Marine Risk Index (MRI) from ensemble forecasts."""
    if merged_df.empty or merged_df[["sst", "salinity", "chlor_a"]].dropna().empty:
        print("⚠️ Skipping risk computation — insufficient forecast data.")
        return pd.DataFrame()

    risk_df = merged_df.copy()
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(risk_df[["sst", "salinity", "chlor_a"]])
    risk_df[["sst_norm", "salinity_norm", "chlor_a_norm"]] = scaled

    # Invert salinity (low salinity = high risk)
    risk_df["salinity_norm"] = 1 - risk_df["salinity_norm"]

    # Weighted MRI
    risk_df["marine_risk_index"] = (
        0.5 * risk_df["sst_norm"]
        + 0.3 * risk_df["chlor_a_norm"]
        + 0.2 * risk_df["salinity_norm"]
    )

    # Categorize risk level
    risk_df["risk_level"] = pd.cut(
        risk_df["marine_risk_index"],
        bins=[0, 0.33, 0.66, 1],
        labels=["Low", "Moderate", "High"]
    )
    return risk_df



# === Visualization ===
def plot_risk_trends(risk_df, lat, lon):
    if risk_df.empty or "time" not in risk_df.columns:
        print(f"⚠️ Skipping plot — no valid risk data for ({lat}, {lon})")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(risk_df["time"], risk_df["marine_risk_index"], label="Marine Risk Index", color="darkred", linewidth=2)
    plt.fill_between(risk_df["time"], 0, risk_df["marine_risk_index"], color="red", alpha=0.2)
    plt.title(f"🌊 Marine Risk Index Forecast ({lat}, {lon})", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Risk Index (0–1)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # ✅ USE THE CORRECT DIRECTORY
    plot_path = os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"🖼️ Saved plot → {plot_path}")




# === Main Pipeline ===
def main(lat, lon):
    print("\n==============================")
    print("🌊 FORECAST & MARINE RISK FUSION")
    print("==============================")

    # Load forecasts
    sst = load_forecast("sea_surface_temperature_max", lat, lon)
    sal = load_forecast("salinity", lat, lon)
    chl = load_forecast("chlor_a", lat, lon)

    # Merge all three
    merged = pd.merge(sst, sal, on="time", suffixes=("_sst", "_sal"))
    merged = pd.merge(merged, chl, on="time")
    merged.rename(columns={
        "ensemble_forecast_sst": "sst",
        "ensemble_forecast_sal": "salinity",
        "ensemble_forecast": "chlor_a"
    }, inplace=True)

    # Compute marine risk
    if merged.empty or merged.shape[0] == 0:
        print(f"⚠️ No valid forecast data to compute risk for ({lat}, {lon}).")
        placeholder_plot = os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png")
        os.makedirs(PLOTS_DIR, exist_ok=True)

        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.text(0.5, 0.5, "No Risk Data Available", fontsize=16, ha="center", va="center")
        plt.title(f"Marine Risk Index — ({lat}, {lon})")
        plt.axis("off")
        plt.savefig(placeholder_plot)
        plt.close()
        print(f"🖼️ Placeholder plot saved → {placeholder_plot}")
        return

    risk_df = compute_risk_index(merged)

    # Save outputs
    out_csv = os.path.join(OUTPUT_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
    risk_df.to_csv(out_csv, index=False)
    print(f"✅ Saved marine risk forecast → {out_csv}")

    plot_risk_trends(risk_df, lat, lon)
    print(f"🖼️ Saved risk index plot → {os.path.join(PLOTS_DIR, f'marine_risk_index_{lat}_{lon}.png')}")

    # Ensure 'time' is datetime
    risk_df["time"] = pd.to_datetime(risk_df["time"], errors="coerce")

    latest = risk_df.iloc[-1]
    print("\n📊 Latest Risk Summary:")
    print(f"   Date: {latest['time'].strftime('%Y-%m-%d')}")
    print(f"   Marine Risk Index: {latest['marine_risk_index']:.3f}")
    print(f"   Risk Level: {latest['risk_level']}")


# === CLI Entry ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    main(args.lat, args.lon)
