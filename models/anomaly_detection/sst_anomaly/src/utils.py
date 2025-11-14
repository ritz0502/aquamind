# utils.py - helper functions for logging and simple ASCII plotting
import os
import sys
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def ensure_dirs():
    Path("../data").mkdir(parents=True, exist_ok=True)
    Path("../outputs/plots").mkdir(parents=True, exist_ok=True)

def print_alert_terminal(message, level="INFO"):
    # simple colorized terminal output (Windows CMD supports ANSI in modern builds)
    prefix = f"[{level}] {datetime.utcnow().isoformat()}Z"
    print(f"\033[1;33m{prefix}\033[0m {message}")

def save_plot_ts(df, location_tag, out_fname):
    # df must have 'time' index and 'sst' column
    plt.figure(figsize=(8,3))
    plt.plot(df.index, df['sst'])
    plt.scatter(df.index[-1], df['sst'].iloc[-1], s=50)
    plt.title(f"SST time series - {location_tag}")
    plt.xlabel("Date")
    plt.ylabel("SST (°C)")
    plt.tight_layout()
    plt.savefig(out_fname)
    plt.close()

def small_ascii_sparkline(series, width=40):
    # tiny sparkline for terminal — maps values to block chars
    vals = series[-width:]
    if len(vals)==0: return ""
    mn, mx = min(vals), max(vals)
    if mx==mn:
        return "▁" * len(vals)
    blocks = "▁▂▃▄▅▆▇█"
    out = ""
    for v in vals:
        idx = int((v-mn)/(mx-mn) * (len(blocks)-1))
        out += blocks[idx]
    return out
