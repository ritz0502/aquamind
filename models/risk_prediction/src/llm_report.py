import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RISK_DIR = os.path.join(DATA_DIR, "risk")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def analyze_trends(df):
    """Analyze trends in SST, salinity, and chlorophyll."""
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
        report.append(f"🌡️ Sea surface temperature has increased by {t['sst_pct']:.2f}% over the past week, indicating warming conditions.")
    elif t["sst_pct"] < -2:
        report.append(f"🌡️ Sea surface temperature has dropped by {abs(t['sst_pct']):.2f}%, suggesting cooler oceanic conditions.")
    else:
        report.append("🌡️ Sea surface temperature remained relatively stable this week.")

    # Salinity
    if t["sal_pct"] > 2:
        report.append(f"🧂 Salinity increased by {t['sal_pct']:.2f}%, indicating higher evaporation or lower freshwater inflow.")
    elif t["sal_pct"] < -2:
        report.append(f"🧂 Salinity decreased by {abs(t['sal_pct']):.2f}%, likely due to precipitation or freshwater discharge.")
    else:
        report.append("🧂 Salinity remained stable and within normal ranges.")

    # Chlorophyll
    if t["chl_pct"] > 10:
        report.append(f"🪸 Chlorophyll-a concentration spiked by {t['chl_pct']:.2f}%, signaling possible algal growth or mild bloom activity.")
    elif t["chl_pct"] < -10:
        report.append(f"🪸 Chlorophyll-a concentration dropped by {abs(t['chl_pct']):.2f}%, suggesting reduced phytoplankton presence.")
    else:
        report.append("🪸 Chlorophyll-a concentration showed minor fluctuations with no major bloom signs.")

    # Risk trend
    if t["risk_trend"] > 0.05:
        report.append("⚠️ Marine Risk Index shows a rising trend — local ocean conditions may become moderately risk-prone.")
    elif t["risk_trend"] < -0.05:
        report.append("✅ Marine Risk Index has decreased slightly — conditions appear to be stabilizing.")
    else:
        report.append("🌊 Marine Risk Index remains steady, indicating balanced marine conditions.")

    return "\n".join(report)


def generate_report(lat, lon):
    """Generate natural language marine risk report."""
    file_path = os.path.join(RISK_DIR, f"marine_risk_forecast_{lat}_{lon}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Risk forecast CSV not found: {file_path}")

    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["time"])
    df = df.dropna(subset=["marine_risk_index"])

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
