# import os
# import argparse
# import pandas as pd
# import numpy as np
# from datetime import datetime
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout
# from sklearn.preprocessing import MinMaxScaler
# import joblib
# import matplotlib.pyplot as plt

# # === Directories ===
# DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
# PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
# MODEL_DIR = os.path.join(DATA_DIR, "models")
# FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
# PLOTS_DIR = os.path.join(DATA_DIR, "plots")

# os.makedirs(MODEL_DIR, exist_ok=True)
# os.makedirs(FORECAST_DIR, exist_ok=True)
# os.makedirs(PLOTS_DIR, exist_ok=True)


# # === Helper Function ===
# def create_sequences(data, seq_len):
#     """Convert data into sliding window sequences for LSTM."""
#     X, y = [], []
#     for i in range(len(data) - seq_len):
#         X.append(data[i:i+seq_len])
#         y.append(data[i+seq_len])
#     return np.array(X), np.array(y)


# def train_lstm_for_variable(df, variable, lat, lon, forecast_days=30, seq_len=14):
#     """Train LSTM for one variable and forecast next N days."""
#     if variable not in df.columns:
#         print(f"⚠️ Skipping {variable}: not found in dataset.")
#         return None

#     print(f"\n🧠 Training LSTM model for {variable}...")

#     df_var = df[["time", variable]].dropna()
#     df_var["time"] = pd.to_datetime(df_var["time"])
#     df_var = df_var.sort_values("time")

#     values = df_var[variable].values.reshape(-1, 1)
#     scaler = MinMaxScaler()
#     scaled = scaler.fit_transform(values)

#     # Prepare sequences
#     X, y = create_sequences(scaled, seq_len)
#     X = X.reshape((X.shape[0], X.shape[1], 1))

#     # Split train/test
#     split = int(len(X) * 0.8)
#     X_train, X_test = X[:split], X[split:]
#     y_train, y_test = y[:split], y[split:]

#     # === LSTM Architecture ===
#     model = Sequential([
#         LSTM(64, return_sequences=True, input_shape=(seq_len, 1)),
#         Dropout(0.2),
#         LSTM(32, return_sequences=False),
#         Dense(16, activation='relu'),
#         Dense(1)
#     ])

#     model.compile(optimizer='adam', loss='mse')
#     history = model.fit(
#         X_train, y_train,
#         validation_data=(X_test, y_test),
#         epochs=50,
#         batch_size=16,
#         verbose=1
#     )

#     # === Save model & scaler ===
#     model_path = os.path.join(MODEL_DIR, f"lstm_{variable}_{lat}_{lon}.h5")
#     scaler_path = os.path.join(MODEL_DIR, f"scaler_{variable}_{lat}_{lon}.pkl")
#     model.save(model_path)
#     joblib.dump(scaler, scaler_path)

#     print(f"✅ Saved LSTM model → {model_path}")
#     print(f"✅ Saved scaler → {scaler_path}")

#     # === Forecast next N days ===
#     last_seq = scaled[-seq_len:]
#     predictions = []
#     for _ in range(forecast_days):
#         input_seq = last_seq.reshape((1, seq_len, 1))
#         pred = model.predict(input_seq, verbose=0)
#         predictions.append(pred[0, 0])
#         last_seq = np.append(last_seq[1:], pred).reshape(seq_len, 1)

#     # Inverse scale
#     predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

#     future_dates = pd.date_range(df_var["time"].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days)
#     forecast_df = pd.DataFrame({"time": future_dates, f"{variable}_forecast": predictions})

#     # Save forecast
#     forecast_path = os.path.join(FORECAST_DIR, f"forecast_lstm_{variable}_{lat}_{lon}.csv")
#     forecast_df.to_csv(forecast_path, index=False)
#     print(f"✅ Saved forecast CSV → {forecast_path}")

#     # Plot
#     plt.figure(figsize=(10, 6))
#     plt.plot(df_var["time"], df_var[variable], label="Historical")
#     plt.plot(future_dates, predictions, label="Forecast", color="orange")
#     plt.title(f"LSTM Forecast for {variable} ({forecast_days} days)")
#     plt.xlabel("Date")
#     plt.ylabel(variable)
#     plt.legend()
#     plt.tight_layout()
#     plot_path = os.path.join(PLOTS_DIR, f"lstm_forecast_{variable}_{lat}_{lon}.png")
#     plt.savefig(plot_path)
#     plt.close()

#     print(f"🖼️ Saved LSTM forecast plot → {plot_path}")


# def main(lat, lon, forecast_days):
#     print("\n==============================")
#     print("🤖 TRAINING LSTM FORECAST MODEL")
#     print("==============================")

#     processed_file = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
#     if not os.path.exists(processed_file):
#         raise FileNotFoundError(f"Processed file not found: {processed_file}")

#     df = pd.read_csv(processed_file)
#     print(f"📂 Loaded processed data: {processed_file}")

#     for var in ["sea_surface_temperature_max", "salinity", "chlor_a"]:
#         train_lstm_for_variable(df, var, lat, lon, forecast_days)

#     print("\n✅ All LSTM models trained and forecasts saved.")


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
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, Input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')


# === Directory Setup ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODEL_DIR = os.path.join(DATA_DIR, "models")
FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(FORECAST_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# === Helper Functions ===
def create_sequences(data, seq_len):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i + seq_len])
        y.append(data[i + seq_len])
    return np.array(X), np.array(y)

def safe_mape(y_true, y_pred):
    """Symmetric MAPE (handles zeros safely)"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_pred) + np.abs(y_true) + 1e-8)) * 100


# === Core LSTM Function ===
def train_lstm_for_variable(df, variable, lat, lon, forecast_days=30, seq_len=14):
    if variable not in df.columns:
        print(f"⚠️ Skipping {variable}: not found in dataset.")
        return

    print(f"\n🧠 Refining LSTM model for {variable}...")

    df_var = df[["time", variable]].dropna()
    df_var["time"] = pd.to_datetime(df_var["time"])
    values = df_var[variable].values.reshape(-1, 1)

    if len(values) < seq_len * 2:
        print(f"⚠️ Not enough data for {variable}. Skipping.")
        return

    # ==== Special Preprocessing for chlor_a ====
    log_transform = False
    if variable == "chlor_a":
        log_transform = True
        # Apply light smoothing (reduce noise)
        df_var[variable] = df_var[variable].rolling(window=3, center=True, min_periods=1).mean()
        # Log transform for stability
        df_var[variable] = np.log1p(df_var[variable])
        values = df_var[variable].values.reshape(-1, 1)

    # === Scaling ===
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values)
    X, y = create_sequences(scaled, seq_len)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # ==== Model Architecture ====
    if variable == "chlor_a":
        # More expressive model for noisy data
        model = Sequential([
            Input(shape=(seq_len, 1)),
            Bidirectional(LSTM(128, return_sequences=True)),
            Dropout(0.4),
            Bidirectional(LSTM(64, return_sequences=False)),
            Dense(64, activation='relu'),
            Dense(1)
        ])
    else:
        # Simpler model for SST and salinity
        model = Sequential([
            Input(shape=(seq_len, 1)),
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            Bidirectional(LSTM(32, return_sequences=False)),
            Dense(32, activation='relu'),
            Dense(1)
        ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')

    early_stop = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=8, min_lr=1e-5)

    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=250,
        batch_size=16,
        verbose=0,
        callbacks=[early_stop, reduce_lr]
    )

    # === Evaluation ===
    y_pred = model.predict(X_test, verbose=0)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = safe_mape(y_test, y_pred)

    print(f"📊 {variable}: RMSE={rmse:.4f}, MAE={mae:.4f}, sMAPE={mape:.2f}%")

    # === Save Model and Scaler ===
    model_path = os.path.join(MODEL_DIR, f"lstm_{variable}_{lat}_{lon}.keras")
    scaler_path = os.path.join(MODEL_DIR, f"scaler_{variable}_{lat}_{lon}.pkl")
    model.save(model_path)
    joblib.dump(scaler, scaler_path)

    # === Forecasting ===
    last_seq = scaled[-seq_len:]
    preds = []
    for _ in range(forecast_days):
        p = model.predict(last_seq.reshape(1, seq_len, 1), verbose=0)
        preds.append(p[0, 0])
        last_seq = np.append(last_seq[1:], p).reshape(seq_len, 1)

    preds = np.array(preds).reshape(-1, 1)
    preds = scaler.inverse_transform(preds).flatten()

    # Invert log transform if applied
    if log_transform:
        preds = np.expm1(preds)
        df_var[variable] = np.expm1(df_var[variable])

    future_dates = pd.date_range(df_var["time"].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days)
    forecast_df = pd.DataFrame({"time": future_dates, f"{variable}_forecast": preds})
    forecast_df.to_csv(os.path.join(FORECAST_DIR, f"forecast_lstm_{variable}_{lat}_{lon}.csv"), index=False)

    # === Plot Validation ===
    plt.figure(figsize=(10, 6))
    plt.plot(df_var["time"].iloc[-len(y_test):], scaler.inverse_transform(y_test.reshape(-1, 1)), label="True")
    plt.plot(df_var["time"].iloc[-len(y_test):], scaler.inverse_transform(y_pred), label="Predicted")
    plt.title(f"LSTM Validation — {variable}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"lstm_refined_validation_{variable}_{lat}_{lon}.png"))
    plt.close()


# === Main Entry Point ===
def main(lat, lon, forecast_days):
    processed = os.path.join(PROCESSED_DIR, f"merged_marine_data_{lat}_{lon}.csv")
    if not os.path.exists(processed):
        raise FileNotFoundError(f"Processed data not found: {processed}")

    df = pd.read_csv(processed)
    for var in ["sea_surface_temperature_max", "salinity", "chlor_a"]:
        train_lstm_for_variable(df, var, lat, lon, forecast_days)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--forecast_days", type=int, default=30)
    args = parser.parse_args()
    main(args.lat, args.lon, args.forecast_days)
