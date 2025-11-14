# main.py - rolling-window adaptive anomaly detection

import os
from datetime import datetime
import pandas as pd

from .utils import ensure_dirs, small_ascii_sparkline, print_alert_terminal
from .data_fetch import load_local_sample
from .anomaly_detector import SSTAnomalyDetector
from .alerting import alert_pipeline


ROLLING_TRAIN_WINDOW = 90     # days used to train model for each test point
TEST_WINDOW = 200             # last N days to evaluate for anomalies


def run_demo():
    ensure_dirs()

    # Load real NOAA or local cached CSV
    df = load_local_sample()
    df = df.sort_values("time").reset_index(drop=True)

    total_days = len(df)
    start_idx = max(0, total_days - TEST_WINDOW)

    print_alert_terminal(
        f"Loaded {total_days} days. Rolling train window = {ROLLING_TRAIN_WINDOW} days; testing last {TEST_WINDOW} days.",
        level="INFO"
    )

    # Store anomaly results here
    results = []

    # Rolling window anomaly loop
    for i in range(start_idx, total_days):
        # rolling train slice: previous 90 days
        train_start = max(0, i - ROLLING_TRAIN_WINDOW)
        train_df = df.iloc[train_start:i]

        # skip if not enough train data
        if len(train_df) < 30:
            continue

        test_point = df.iloc[i:i+1]

        # Fit model and score 1 point
        detector = SSTAnomalyDetector()
        detector.fit(train_df[['time', 'sst']])
        scored = detector.score(test_point[['time', 'sst']])

        results.append(scored)

    # Combine scored results into df
    all_scored = pd.concat(results).reset_index(drop=True)

    # Print sparkline
    print_alert_terminal(
        "Recent SST sparkline: " + small_ascii_sparkline(df['sst']),
        level="INFO"
    )

    # Find anomalies in rolling window
    flagged = all_scored[all_scored['flag']]

    if flagged.empty:
        print_alert_terminal("No anomalies detected in the test window.", level="OK")
        return

    # Trigger pipeline for each anomaly
    for idx, row in flagged.iterrows():
        event_date = row['time']

        # Build 30-day context window around the anomaly
        ctx_start = max(0, idx - 30)
        ctx_df = all_scored.iloc[ctx_start: idx+1].reset_index(drop=True)

        location_tag = "lat:lon"  # replace with real coordinates if needed
        alert_pipeline(row, ctx_df, location_tag=location_tag)


if __name__ == "__main__":
    run_demo()
