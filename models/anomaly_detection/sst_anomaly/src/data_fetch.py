# data_fetch.py - fetch a small point time series from NOAA ERDDAP or generate synthetic data
import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from .config import TRAIN_WINDOW_DAYS, DEFAULT_LAT, DEFAULT_LON, DEFAULT_START_DATE, DEFAULT_END_DATE

load_dotenv()

DATA_DIR = Path(os.path.join(os.path.dirname(__file__), "..", "data"))

def generate_synthetic(lat=DEFAULT_LAT, lon=DEFAULT_LON, days=120, seed=42):
    np.random.seed(seed)
    base = 27.0 + 2.0 * np.sin(np.linspace(0, 6.28, days))  # slow seasonal
    noise = np.random.normal(0, 0.2, size=days)
    # Insert a spike near the end
    spike = np.zeros(days)
    spike_idx = days - 3
    spike[spike_idx:] = np.array([0.0, 1.8, 2.2])  # a 2°C rise event
    sst = base + noise + spike
    times = [ (datetime.utcnow() - timedelta(days=(days-1-i))).date().isoformat() for i in range(days) ]
    df = pd.DataFrame({"time": pd.to_datetime(times), "sst": sst})
    file_path = DATA_DIR / "sample_sst_point.csv"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    return df

def fetch_noaa_point(lat=DEFAULT_LAT, lon=DEFAULT_LON, start_date=None, end_date=None):
    """
    Example ERDDAP-style fetch: user may need to adapt to a working ERDDAP server.
    For demo we include a placeholder; if ERDDAP accessible use a properly formatted URL.
    """
    # Example: NOAA APDRC or other ERDDAP can serve CSV for a small bounding box/time:
    # URL style varies by server; user should replace below with their ERDDAP dataset id.
    raise NotImplementedError(
        "fetch_noaa_point is a helper template. For small-point fetch use ERDDAP griddap CSV URL "
        "for an available dataset. See README for an example URL and how to adapt it."
    )

def load_local_sample():
    fp = DATA_DIR / "oisst_point.csv"
    if not fp.exists():
        raise FileNotFoundError("oisst_point.csv not found in data/ folder")

    # Skip row 1 (units row)
    df = pd.read_csv(fp, skiprows=[1])

    # Ensure correct columns
    required = ["time", "sst"]
    if not all(col in df.columns for col in required):
        raise ValueError(f"CSV missing required columns: {required}")

    # Parse time column
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")

    # Remove rows where time parsing failed
    df = df.dropna(subset=["time"])

    # Sort chronologically
    df = df.sort_values("time").reset_index(drop=True)

    # Keep only what we need
    df = df[["time", "sst"]]

    return df

