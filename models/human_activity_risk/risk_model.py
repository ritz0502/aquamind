# import joblib
# from sklearn.ensemble import RandomForestRegressor

# MODEL_FILE = "activity_risk_model.pkl"

# def train_model(df):
#     """
#     df must contain columns: ports, industries, hotels, ships, activity_score
#     Returns trained model (RandomForest) and saves to disk.
#     """
#     X = df[["ports", "industries", "hotels", "ships"]]
#     y = df["activity_score"]
#     model = RandomForestRegressor(n_estimators=120, random_state=42)
#     model.fit(X, y)
#     joblib.dump(model, MODEL_FILE)
#     print(f"✅ Model trained and saved to {MODEL_FILE}")
#     return model

# def load_model():
#     try:
#         return joblib.load(MODEL_FILE)
#     except Exception:
#         return None



# import joblib
# import numpy as np
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error, r2_score

# MODEL_PATH = "activity_risk_model.pkl"
# SCALER_PATH = "activity_scaler.pkl"

# def train_model(df):
#     """
#     Trains a RandomForestRegressor on features -> activity_score (0-100).
#     Saves model + scaler and returns (model, scaler).
#     """
#     # features in df already normalized in main.py (but to be robust we fit scaler on original counts)
#     X = df[["ports", "industries", "hotels", "ships"]].values.astype(float)
#     y = df["activity_score"].values.astype(float)

#     # Fit a MinMaxScaler on current X (ensures model can be used later with raw counts if we choose)
#     scaler = MinMaxScaler()
#     X_scaled = scaler.fit_transform(X)

#     # train/test split
#     X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.15, random_state=42)

#     model = RandomForestRegressor(
#         n_estimators=300,
#         max_depth=12,
#         min_samples_leaf=3,
#         random_state=42,
#         n_jobs=-1
#     )
#     model.fit(X_train, y_train)

#     # validation metrics
#     y_pred = model.predict(X_val)
#     mae = mean_absolute_error(y_val, y_pred)
#     r2 = r2_score(y_val, y_pred)
#     print(f"✅ Model trained. Validation MAE: {mae:.3f}, R2: {r2:.3f}")

#     # persist
#     joblib.dump(model, MODEL_PATH)
#     joblib.dump(scaler, SCALER_PATH)
#     print(f"✅ Model saved to {MODEL_PATH}, scaler saved to {SCALER_PATH}")

#     return model, scaler


# def load_model(model_path=MODEL_PATH, scaler_path=SCALER_PATH):
#     model = joblib.load(model_path)
#     scaler = joblib.load(scaler_path)
#     return model, scaler





















# risk_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

FEATURE_COLS = ["ports", "industries", "hotels", "ships"]

def train_model(df):
    X = df[FEATURE_COLS].values
    y = df["activity_score"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_val, y_train, y_val = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Save
    joblib.dump(model, "activity_risk_model.pkl")
    joblib.dump(scaler, "activity_scaler.pkl")

    # Evaluate
    mae = abs(model.predict(X_val) - y_val).mean()
    r2 = model.score(X_val, y_val)
    print(f"Validation MAE: {mae:.3f}, R2: {r2:.3f}")

    return model, scaler

def load_model():
    import joblib
    return joblib.load("activity_risk_model.pkl")

def load_scaler():
    import joblib
    return joblib.load("activity_scaler.pkl")
