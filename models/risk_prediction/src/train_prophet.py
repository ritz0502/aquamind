# import os
# import argparse
# import pandas as pd
# from prophet import Prophet
# import joblib
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt

# # === Directory Setup ===
# DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
# MODEL_DIR = os.path.join(DATA_DIR, "models")
# FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
# PLOTS_DIR = os.path.join(DATA_DIR, "plots")

# os.makedirs(MODEL_DIR, exist_ok=True)
# os.makedirs(FORECAST_DIR, exist_ok=True)
# os.makedirs(PLOTS_DIR, exist_ok=True)


# def train_and_forecast(variable, df, lat, lon, forecast_days=30):
#     """Train Prophet model for one variable, forecast, save, and visualize."""

#     if variable not in df.columns:
#         print(f"⚠️ Skipping {variable}: not found in dataset.")
#         return None

#     print(f"\n📈 Training Prophet model for {variable}...")

#     # Prophet expects 'ds' (datetime) and 'y' (target)
#     df_prophet = df.rename(columns={"time": "ds", variable: "y"})
#     df_prophet = df_prophet.dropna(subset=["y"])

#     if df_prophet.empty:
#         print(f"⚠️ No data available for {variable}, skipping.")
#         return None

#     # === Train Prophet ===
#     model = Prophet(
#         daily_seasonality=True,
#         yearly_seasonality=False,
#         weekly_seasonality=False,
#         changepoint_prior_scale=0.1,
#     )
#     model.fit(df_prophet)

#     # === Forecast Future ===
#     future = model.make_future_dataframe(periods=forecast_days)
#     forecast = model.predict(future)

#     # === Save Model & Forecast ===
#     model_path = os.path.join(MODEL_DIR, f"prophet_{variable}_{lat}_{lon}.pkl")
#     forecast_path = os.path.join(FORECAST_DIR, f"forecast_{variable}_{lat}_{lon}.csv")

#     joblib.dump(model, model_path)
#     forecast.to_csv(forecast_path, index=False)

#     print(f"✅ Saved Prophet model → {model_path}")
#     print(f"✅ Saved forecast CSV → {forecast_path}")

#     # === Visualization ===
#     fig, ax = plt.subplots(figsize=(10, 6))
#     model.plot(forecast, ax=ax)
#     plt.title(f"{variable.upper()} Forecast ({forecast_days} days) — {lat}, {lon}")
#     plt.xlabel("Date")
#     plt.ylabel(variable)
#     plot_path = os.path.join(PLOTS_DIR, f"forecast_{variable}_{lat}_{lon}.png")
#     plt.savefig(plot_path)
#     plt.close()

#     print(f"🖼️ Saved forecast plot → {plot_path}")

#     return forecast


# def main(lat, lon, forecast_days):
#     print("\n==============================")
#     print("🤖 TRAINING PROPHET FORECAST MODEL")
#     print("==============================")

#     processed_file = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
#     if not os.path.exists(processed_file):
#         raise FileNotFoundError(f"Processed file not found: {processed_file}")

#     df = pd.read_csv(processed_file, parse_dates=["time"])
#     print(f"📂 Loaded processed data: {processed_file}")

#     # Train and forecast for key variables
#     for var in ["sea_surface_temperature_max", "salinity", "chlor_a"]:
#         train_and_forecast(var, df, lat, lon, forecast_days)

#     print("\n✅ All Prophet models trained and forecasts saved.")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--lat", type=float, required=True)
#     parser.add_argument("--lon", type=float, required=True)
#     parser.add_argument("--forecast_days", type=int, default=30)
#     args = parser.parse_args()
#     main(args.lat, args.lon, args.forecast_days)

















































import os
import argparse
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import sys
sys.stdout.reconfigure(encoding='utf-8')


# === Directories ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")
os.makedirs(FORECAST_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


def evaluate_prophet(model, df_prophet, variable, lat, lon):
    """Evaluate Prophet with rolling cross-validation."""
    print(f"\n📊 Evaluating Prophet model for {variable}...")
    try:
        df_cv = cross_validation(model, initial='30 days', period='7 days', horizon='15 days')
        df_p = performance_metrics(df_cv)
        print(df_p[["horizon", "mse", "mae", "rmse", "mape"]].head())
    except Exception as e:
        print(f"⚠️ Cross-validation skipped due to: {e}")


def train_and_forecast_prophet(df, variable, lat, lon, forecast_days=30):
    """Train Prophet and forecast with evaluation."""
    df = df[["time", variable]].dropna()
    df = df.rename(columns={"time": "ds", variable: "y"})
    df["ds"] = pd.to_datetime(df["ds"])

    

    model = Prophet(daily_seasonality=True)
    if df.dropna().shape[0] < 2:
        print(f"⚠️ Skipping Prophet training for {variable} — insufficient data ({df.dropna().shape[0]} valid rows).")
        return

    model.fit(df)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    # === Save forecast ===
    out_csv = os.path.join(FORECAST_DIR, f"forecast_prophet_{variable}_{lat}_{lon}.csv")
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(out_csv, index=False)
    print(f"✅ Saved Prophet forecast → {out_csv}")

    # === Evaluate ===
    evaluate_prophet(model, df, variable, lat, lon)

    # === Validation plot ===
    plt.figure(figsize=(10, 6))
    plt.plot(df["ds"], df["y"], label="Actual", color="blue")
    plt.plot(forecast["ds"], forecast["yhat"], label="Predicted", color="orange")
    plt.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.3, color="orange")
    plt.title(f"{variable.upper()} Prophet Forecast ({forecast_days} days) — {lat}, {lon}")
    plt.xlabel("Date")
    plt.ylabel(variable)
    plt.legend()
    plot_path = os.path.join(PLOTS_DIR, f"prophet_validation_{variable}_{lat}_{lon}.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    print(f"🖼️ Saved Prophet validation plot → {plot_path}")


def main(lat, lon, forecast_days):
    processed_path = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
    if not os.path.exists(processed_path):
        raise FileNotFoundError(f"Processed data not found: {processed_path}")

    df = pd.read_csv(processed_path)

    for var in ["sea_surface_temperature_max", "salinity", "chlor_a"]:
        print(f"\n==============================")
        print(f"🔮 Training Prophet for {var}")
        print("==============================")
        train_and_forecast_prophet(df, var, lat, lon, forecast_days)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--forecast_days", type=int, default=30)
    parser.add_argument("--fast_mode", action="store_true", help="Enable faster training (skips diagnostics)")
    args = parser.parse_args()
    main(args.lat, args.lon, args.forecast_days)
