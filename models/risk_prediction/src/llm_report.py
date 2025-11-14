import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

# === Directory Setup ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RISK_DIR = os.path.join(DATA_DIR, "risk")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def analyze_trends(df):
    """Analyze trends in SST, salinity, and chlorophyll."""
    if len(df) < 14:
        print("⚠️ Not enough data points to compute weekly trends.")
        return {k: 0 for k in ["sst_change","sst_pct","sal_change","sal_pct","chl_change","chl_pct","risk_trend"]}

    last_week = df.tail(7)
    prev_week = df.iloc[-14:-7]

    def trend(col):
        recent = last_week[col].mean()
        prev = prev_week[col].mean()
        change = recent - prev
        pct = (change / prev) * 100 if prev != 0 else 0
        return change, pct

    sst_change, sst_pct = trend("sst")
    sal_change, sal_pct = trend("salinity")
    chl_change, chl_pct = trend("chlor_a")

    risk_recent = last_week["marine_risk_index"].mean()
    risk_prev = prev_week["marine_risk_index"].mean()
    risk_trend = risk_recent - risk_prev

    return {
        "sst_change": sst_change,
        "sst_pct": sst_pct,
        "sal_change": sal_change,
        "sal_pct": sal_pct,
        "chl_change": chl_change,
        "chl_pct": chl_pct,
        "risk_trend": risk_trend
    }


def interpret_trends(t):
    """Turn numeric changes into natural-language insights."""
    report = []

    # SST
    if t["sst_pct"] > 2:
        report.append(f"🌡️ Sea surface temperature increased by {t['sst_pct']:.2f}% this week.")
    elif t["sst_pct"] < -2:
        report.append(f"🌡️ Sea surface temperature dropped by {abs(t['sst_pct']):.2f}%.")
    else:
        report.append("🌡️ Sea surface temperature remained relatively stable this week.")

    # Salinity
    if t["sal_pct"] > 2:
        report.append(f"🧂 Salinity increased by {t['sal_pct']:.2f}%, possibly due to evaporation.")
    elif t["sal_pct"] < -2:
        report.append(f"🧂 Salinity decreased by {abs(t['sal_pct']):.2f}%, likely due to rainfall or inflow.")
    else:
        report.append("🧂 Salinity remained stable and within normal ranges.")

    # Chlorophyll
    if t["chl_pct"] > 10:
        report.append(f"🪸 Chlorophyll-a concentration spiked by {t['chl_pct']:.2f}%, suggesting mild bloom activity.")
    elif t["chl_pct"] < -10:
        report.append(f"🪸 Chlorophyll-a concentration dropped by {abs(t['chl_pct']):.2f}%, suggesting reduced phytoplankton.")
    else:
        report.append("🪸 Chlorophyll-a concentration showed minor fluctuations with no major bloom signs.")

    # Risk trend
    if t["risk_trend"] > 0.05:
        report.append("⚠️ Marine Risk Index is rising — local conditions may become moderately risk-prone.")
    elif t["risk_trend"] < -0.05:
        report.append("✅ Marine Risk Index has decreased slightly — conditions appear to be stabilizing.")
    else:
        report.append("🌊 Marine Risk Index remains steady, indicating balanced marine conditions.")

    return "\n".join(report)


def generate_report(lat, lon):
    """Generate natural language marine risk report."""
    file_path = os.path.join(RISK_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")

    if not os.path.exists(file_path):
        print(f"⚠️ No risk forecast file found for ({lat}, {lon}).")
        return
    if os.path.getsize(file_path) == 0:
        print(f"⚠️ Empty risk forecast file for ({lat}, {lon}) — skipping report generation.")
        return

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"⚠️ CSV is empty or corrupted — skipping report for ({lat}, {lon}).")
        return

    if df.empty or "marine_risk_index" not in df.columns:
        print(f"⚠️ Risk data empty or incomplete for ({lat}, {lon}).")
        return

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["marine_risk_index"])

    if df.empty:
        print(f"⚠️ No valid data to report for ({lat}, {lon}).")
        return

    trends = analyze_trends(df)
    interpretation = interpret_trends(trends)

    latest = df.iloc[-1]
    overall_risk = latest["risk_level"]
    avg_index = df["marine_risk_index"].mean()

    summary = f"""
==============================
🌊 MARINE RISK INTELLIGENCE REPORT
==============================
📍 Coordinates: ({lat}, {lon})
📅 Last Updated: {latest['time'].strftime('%Y-%m-%d')}

📊 Current Marine Risk Level: {overall_risk.upper()}
📈 Average Marine Risk Index: {avg_index:.3f}

--- Trend Summary ---
{interpretation}

🧭 Model Ensemble: Prophet + LSTM (Weighted Fusion)
🧩 Data Sources: Open-Meteo Marine API, Copernicus Marine Service
💡 Notes: Use this report to monitor changes in marine stability,
algal bloom potential, and near-surface thermal/salinity stress.

Report generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
==============================
"""

    out_path = os.path.join(REPORTS_DIR, f"marine_risk_report_{lat}_{lon}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(summary)
    print(f"✅ Saved text report → {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    args = parser.parse_args()
    generate_report(args.lat, args.lon)
