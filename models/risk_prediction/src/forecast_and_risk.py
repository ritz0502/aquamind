<<<<<<< HEAD
=======

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
<<<<<<< HEAD
=======
from datetime import datetime
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
from sklearn.preprocessing import MinMaxScaler
import sys
sys.stdout.reconfigure(encoding='utf-8')

<<<<<<< HEAD
# ----------------------------------------------------
# Directories
# ----------------------------------------------------
=======

# === Directory Setup ===
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
OUTPUT_DIR = os.path.join(DATA_DIR, "risk")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


<<<<<<< HEAD
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
=======
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
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8

    # Load forecasts
    sst = load_forecast("sea_surface_temperature_max", lat, lon)
    sal = load_forecast("salinity", lat, lon)
    chl = load_forecast("chlor_a", lat, lon)

<<<<<<< HEAD
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


=======
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
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    main(args.lat, args.lon)
