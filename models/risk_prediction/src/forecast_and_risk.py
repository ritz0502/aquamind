import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------
# Directories
# ----------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
OUTPUT_DIR = os.path.join(DATA_DIR, "risk")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


# ----------------------------------------------------
# LOAD FORECASTS (robust)
# ----------------------------------------------------
def load_forecast(variable, lat, lon):
    """Loads Prophet + LSTM forecasts and merges them cleanly."""
    
    prophet_file = os.path.join(
        FORECAST_DIR, f"forecast_prophet_{variable}_{lat}_{lon}.csv"
    )
    lstm_file = os.path.join(
        FORECAST_DIR, f"forecast_lstm_{variable}_{lat}_{lon}.csv"
    )

    # ---------------- Prophet ----------------
    if os.path.exists(prophet_file):
        prophet = pd.read_csv(prophet_file)
        prophet.rename(columns={"ds": "time", "yhat": "prophet"}, inplace=True)
    else:
        print(f"⚠️ Prophet missing for {variable}")
        prophet = pd.DataFrame(columns=["time", "prophet"])

    # ---------------- LSTM ----------------
    if os.path.exists(lstm_file):
        lstm = pd.read_csv(lstm_file)

        # Normalize column names:
        if "time" not in lstm.columns and "date" in lstm.columns:
            lstm.rename(columns={"date": "time"}, inplace=True)

        # Find forecast column
        fc_cols = [c for c in lstm.columns if "forecast" in c.lower() or "prediction" in c.lower()]

        if fc_cols:
            lstm.rename(columns={fc_cols[0]: "lstm"}, inplace=True)
        else:
            lstm["lstm"] = np.nan

    else:
        print(f"⚠️ LSTM missing for {variable}")
        lstm = pd.DataFrame(columns=["time", "lstm"])

    # Merge
    df = pd.merge(prophet[["time", "prophet"]],
                  lstm[["time", "lstm"]],
                  on="time",
                  how="outer").sort_values("time")

    # Ensemble average
    df["forecast"] = df[["prophet", "lstm"]].mean(axis=1)

    return df[["time", "forecast"]]


# ----------------------------------------------------
# RISK COMPUTATION
# ----------------------------------------------------
def compute_risk(df):
    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(df[["sst", "salinity", "chlor_a"]])
    df["sst_norm"], df["salinity_norm"], df["chlor_a_norm"] = scaled.T

    # Inverse salinity (low salinity = higher risk)
    df["salinity_norm"] = 1 - df["salinity_norm"]

    df["marine_risk_index"] = (
        0.5 * df["sst_norm"] +
        0.3 * df["chlor_a_norm"] +
        0.2 * df["salinity_norm"]
    )

    df["risk_level"] = pd.cut(
        df["marine_risk_index"],
        bins=[0, 0.33, 0.66, 1],
        labels=["Low", "Moderate", "High"]
    )

    return df


# ----------------------------------------------------
# PLOTS
# ----------------------------------------------------
def plot_risk(df, lat, lon):
    if df.empty:
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["marine_risk_index"], linewidth=2, color="red")
    plt.fill_between(df["time"], 0, df["marine_risk_index"], alpha=0.2, color="red")
    plt.title(f"Marine Risk Index ({lat}, {lon})")
    plt.xlabel("Date")
    plt.ylabel("MRI (0–1)")
    plt.grid(True)

    out = os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png")
    plt.savefig(out)
    plt.close()

    print(f"🖼️ Saved plot → {out}")


# ----------------------------------------------------
# MAIN
# ----------------------------------------------------
def main(lat, lon):
    print("\n============================")
    print("🌊 FORECAST & MARINE RISK FUSION")
    print("============================")

    # Load forecasts
    sst = load_forecast("sea_surface_temperature_max", lat, lon)
    sal = load_forecast("salinity", lat, lon)
    chl = load_forecast("chlor_a", lat, lon)

    # Merge all
    merged = (
        sst.rename(columns={"forecast": "sst"})
        .merge(sal.rename(columns={"forecast": "salinity"}), on="time", how="outer")
        .merge(chl.rename(columns={"forecast": "chlor_a"}), on="time", how="outer")
    )

    merged["time"] = pd.to_datetime(merged["time"])
    merged = merged.sort_values("time").dropna()

    if merged.empty:
        print("⚠️ No usable forecast data, creating placeholder plot.")
        plt.figure(figsize=(10, 4))
        plt.text(0.5, 0.5, "No Risk Data Available",
                 ha="center", va="center", fontsize=16)
        plt.axis("off")
        out = os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png")
        plt.savefig(out)
        plt.close()
        return

    # Compute risk
    risk_df = compute_risk(merged)

    # Save
    out_csv = os.path.join(OUTPUT_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
    risk_df.to_csv(out_csv, index=False)
    print(f"✅ Saved MRI CSV → {out_csv}")

    # Plot
    plot_risk(risk_df, lat, lon)

    print("\n📊 Latest Risk Summary:")
    print(risk_df.tail(1)[["time", "marine_risk_index", "risk_level"]].to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    main(args.lat, args.lon)
