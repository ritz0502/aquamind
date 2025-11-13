# import os
# import argparse
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime
# from sklearn.preprocessing import MinMaxScaler

# # === Directory Setup ===
# DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
# OUTPUT_DIR = os.path.join(DATA_DIR, "risk")
# PLOTS_DIR = os.path.join(DATA_DIR, "plots")

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(PLOTS_DIR, exist_ok=True)


# # === Load and Merge Forecasts ===
# def load_forecast(variable, lat, lon):
#     """Load Prophet and LSTM forecasts for one variable and merge safely."""
#     prophet_path = os.path.join(FORECAST_DIR, f"forecast_prophet_{variable}_{lat}_{lon}.csv")
#     lstm_path = os.path.join(FORECAST_DIR, f"forecast_lstm_{variable}_{lat}_{lon}.csv")

#     if not os.path.exists(prophet_path):
#         raise FileNotFoundError(f"❌ Prophet forecast missing: {prophet_path}")
#     if not os.path.exists(lstm_path):
#         raise FileNotFoundError(f"❌ LSTM forecast missing: {lstm_path}")

#     df_p = pd.read_csv(prophet_path)
#     df_l = pd.read_csv(lstm_path)

#     # --- Fix column naming inconsistencies ---
#     if "ds" in df_p.columns:
#         df_p.rename(columns={"ds": "time"}, inplace=True)
#     elif "date" in df_p.columns:
#         df_p.rename(columns={"date": "time"}, inplace=True)

#     if "yhat" in df_p.columns:
#         df_p.rename(columns={"yhat": "prophet_forecast"}, inplace=True)

#     if "date" in df_l.columns:
#         df_l.rename(columns={"date": "time"}, inplace=True)
#     elif "ds" in df_l.columns:
#         df_l.rename(columns={"ds": "time"}, inplace=True)

#     # find forecast column in LSTM file
#     forecast_cols = [c for c in df_l.columns if "forecast" in c.lower()]
#     if forecast_cols:
#         df_l.rename(columns={forecast_cols[0]: "lstm_forecast"}, inplace=True)
#     else:
#         raise KeyError(f"⚠️ No forecast column found in LSTM file for {variable}")

#     # ensure 'time' column exists in both
#     if "time" not in df_p.columns or "time" not in df_l.columns:
#         raise KeyError("❌ Both Prophet and LSTM CSVs must have a 'time' column.")

#     # merge
#     df = pd.merge(df_p[["time", "prophet_forecast"]], df_l[["time", "lstm_forecast"]], on="time", how="outer")
#     df["time"] = pd.to_datetime(df["time"])
#     df.sort_values("time", inplace=True)

#     # weighted ensemble (more weight to LSTM)
#     df["ensemble_forecast"] = 0.6 * df["lstm_forecast"] + 0.4 * df["prophet_forecast"]

#     return df[["time", "ensemble_forecast"]]


# # === Risk Computation ===
# def compute_risk_index(merged_df):
#     """Compute Marine Risk Index from ensemble forecasts."""
#     risk_df = merged_df.copy()

#     scaler = MinMaxScaler()
#     scaled = scaler.fit_transform(risk_df[["sst", "salinity", "chlor_a"]])
#     risk_df[["sst_norm", "salinity_norm", "chlor_a_norm"]] = scaled

#     # Invert salinity (low salinity => high risk)
#     risk_df["salinity_norm"] = 1 - risk_df["salinity_norm"]

#     # Weighted marine risk index
#     risk_df["marine_risk_index"] = (
#         0.5 * risk_df["sst_norm"]
#         + 0.3 * risk_df["chlor_a_norm"]
#         + 0.2 * risk_df["salinity_norm"]
#     )

#     risk_df["risk_level"] = pd.cut(
#         risk_df["marine_risk_index"],
#         bins=[0, 0.33, 0.66, 1],
#         labels=["Low", "Moderate", "High"]
#     )

#     return risk_df


# # === Visualization ===
# def plot_risk_trends(risk_df, lat, lon):
#     plt.figure(figsize=(12, 6))
#     plt.plot(risk_df["time"], risk_df["marine_risk_index"], label="Marine Risk Index", color="darkred", linewidth=2)
#     plt.fill_between(risk_df["time"], 0, risk_df["marine_risk_index"], color="red", alpha=0.2)
#     plt.title(f"🌊 Marine Risk Index Forecast ({lat}, {lon})", fontsize=14)
#     plt.xlabel("Date")
#     plt.ylabel("Risk Index (0–1)")
#     plt.grid(True, linestyle="--", alpha=0.6)
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png"))
#     plt.close()


# # === Main Pipeline ===
# def main(lat, lon):
#     print("\n==============================")
#     print("🌊 FORECAST & MARINE RISK FUSION")
#     print("==============================")

#     sst = load_forecast("sea_surface_temperature_max", lat, lon)
#     sal = load_forecast("salinity", lat, lon)
#     chl = load_forecast("chlor_a", lat, lon)

#     merged = pd.merge(sst, sal, on="time", suffixes=("_sst", "_sal"))
#     merged = pd.merge(merged, chl, on="time")
#     merged.rename(columns={
#         "ensemble_forecast_sst": "sst",
#         "ensemble_forecast_sal": "salinity",
#         "ensemble_forecast": "chlor_a"
#     }, inplace=True)

#     risk_df = compute_risk_index(merged)

#     out_csv = os.path.join(OUTPUT_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
#     risk_df.to_csv(out_csv, index=False)
#     print(f"✅ Saved marine risk forecast → {out_csv}")

#     plot_risk_trends(risk_df, lat, lon)
#     print(f"🖼️ Saved risk index plot → data/plots/marine_risk_index_{lat}_{lon}.png")

#     latest = risk_df.iloc[-1]
#     print("\n📊 Latest Risk Summary:")
#     print(f"   Date: {latest['time'].strftime('%Y-%m-%d')}")
#     print(f"   Marine Risk Index: {latest['marine_risk_index']:.3f}")
#     print(f"   Risk Level: {latest['risk_level']}")


# # === CLI Entry ===
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--lat", type=float, required=True)
#     parser.add_argument("--lon", type=float, required=True)
#     args = parser.parse_args()
#     main(args.lat, args.lon)










import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

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

    if not os.path.exists(prophet_path):
        raise FileNotFoundError(f"❌ Prophet forecast missing: {prophet_path}")
    if not os.path.exists(lstm_path):
        raise FileNotFoundError(f"❌ LSTM forecast missing: {lstm_path}")

    # Load both
    df_p = pd.read_csv(prophet_path)
    df_l = pd.read_csv(lstm_path)

    # Prophet columns: ds, yhat
    if "ds" not in df_p.columns or "yhat" not in df_p.columns:
        raise KeyError(f"Prophet forecast for {variable} missing expected columns ['ds', 'yhat']")
    df_p.rename(columns={"ds": "time", "yhat": "prophet_forecast"}, inplace=True)

    # LSTM columns: time, forecast_...
    if "time" not in df_l.columns:
        raise KeyError(f"LSTM forecast for {variable} missing 'time' column.")
    forecast_cols = [c for c in df_l.columns if "forecast" in c.lower()]
    if not forecast_cols:
        raise KeyError(f"LSTM forecast for {variable} missing forecast column.")
    df_l.rename(columns={forecast_cols[0]: "lstm_forecast"}, inplace=True)

    # Merge
    df = pd.merge(df_p[["time", "prophet_forecast"]], df_l[["time", "lstm_forecast"]], on="time", how="outer")
    df["time"] = pd.to_datetime(df["time"])
    df.sort_values("time", inplace=True)

    # Weighted ensemble (LSTM 60%, Prophet 40%)
    df["ensemble_forecast"] = 0.6 * df["lstm_forecast"] + 0.4 * df["prophet_forecast"]

    return df[["time", "ensemble_forecast"]]


# === Risk Computation ===
def compute_risk_index(merged_df):
    """Compute Marine Risk Index (MRI) from ensemble forecasts."""
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
    """Plot Marine Risk Index forecast."""
    plt.figure(figsize=(12, 6))
    plt.plot(
        risk_df["time"],
        risk_df["marine_risk_index"],
        label="Marine Risk Index",
        color="darkred",
        linewidth=2
    )
    plt.fill_between(
        risk_df["time"],
        0,
        risk_df["marine_risk_index"],
        color="red",
        alpha=0.2
    )
    plt.title(f"🌊 Marine Risk Index Forecast ({lat}, {lon})", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Risk Index (0–1)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"marine_risk_index_{lat}_{lon}.png"))
    plt.close()


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
    risk_df = compute_risk_index(merged)

    # Save outputs
    out_csv = os.path.join(OUTPUT_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
    risk_df.to_csv(out_csv, index=False)
    print(f"✅ Saved marine risk forecast → {out_csv}")

    plot_risk_trends(risk_df, lat, lon)
    print(f"🖼️ Saved risk index plot → data/plots/marine_risk_index_{lat}_{lon}.png")

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
