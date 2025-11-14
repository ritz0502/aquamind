import os
import argparse
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")
os.makedirs(FORECAST_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


def evaluate_model(model, df, variable, lat, lon):
    """Evaluate Prophet model."""
    print(f"📊 Evaluating Prophet for {variable}...")
    try:
        df_cv = cross_validation(
            model,
            initial="30 days",
            period="7 days",
            horizon="15 days"
        )
        perf = performance_metrics(df_cv)
        print(perf[["horizon", "mse", "rmse", "mae", "mape"]].head())
    except Exception as e:
        print(f"⚠️ Skipped evaluation: {e}")


def train_and_forecast(df, variable, lat, lon, forecast_days, fast_mode=False):
    """Train Prophet for a single variable."""
    if variable not in df.columns:
        print(f"⚠️ Skipping {variable}: not in dataset.")
        return

    temp = df[["time", variable]].dropna()
    if temp.empty or temp[variable].nunique() < 2:
        print(f"⚠️ Skipping Prophet for {variable}: insufficient data.")
        return

    temp = temp.rename(columns={"time": "ds", variable: "y"})
    temp["ds"] = pd.to_datetime(temp["ds"])

    print(f"\n🔮 Training Prophet for {variable}...")

    model = Prophet(daily_seasonality=True)
    model.fit(temp)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    out_csv = os.path.join(
        FORECAST_DIR,
        f"forecast_prophet_{variable}_{lat}_{lon}.csv"
    )
    forecast[["ds", "yhat"]].to_csv(out_csv, index=False)
    print(f"✅ Saved → {out_csv}")

    # Skip evaluation in fast mode
    if not fast_mode:
        evaluate_model(model, temp, variable, lat, lon)

    # PLOT
    plt.figure(figsize=(10, 5))
    plt.plot(temp["ds"], temp["y"], label="Actual", color="blue")
    plt.plot(forecast["ds"], forecast["yhat"], label="Forecast", color="orange")
    plt.title(f"{variable.upper()} Forecast — ({lat}, {lon})")
    plt.grid(True)
    plot_path = os.path.join(PLOTS_DIR, f"prophet_validation_{variable}_{lat}_{lon}.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"🖼️ Saved plot → {plot_path}")


def main(lat, lon, forecast_days, fast_mode):
    processed_file = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")

    if not os.path.exists(processed_file):
        raise FileNotFoundError(f"Processed file missing: {processed_file}")

    df = pd.read_csv(processed_file)
    df["time"] = pd.to_datetime(df["time"])

    print("\n==============================")
    print("🔮 RUNNING PROPHET TRAINING")
    print("==============================")

    VARIABLES = [
        "sea_surface_temperature_max",
        "salinity",
        "chlor_a"
    ]

    for var in VARIABLES:
        train_and_forecast(df, var, lat, lon, forecast_days, fast_mode)

    print("\n✅ Prophet training completed.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--forecast_days", type=int, default=30)
    parser.add_argument("--fast_mode", action="store_true")
    args = parser.parse_args()

    main(args.lat, args.lon, args.forecast_days, args.fast_mode)
