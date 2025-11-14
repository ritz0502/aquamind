# alerting.py
import os
from datetime import datetime
import matplotlib.pyplot as plt

from .utils import print_alert_terminal

PLOT_DIR = "../outputs/plots"


def save_context_plot(ctx_df, event_date, location_tag):
    """Plot the last ~30 days of SST around the anomaly and save PNG."""

    if ctx_df.empty:
        return None

    plt.figure(figsize=(8, 4))
    plt.plot(ctx_df["time"], ctx_df["sst"], linewidth=2)
    plt.axvline(event_date, color="red", linestyle="--", linewidth=1.5)
    plt.title(f"SST Anomaly Context @ {location_tag} ({event_date.date()})")
    plt.xlabel("Date")
    plt.ylabel("SST (°C)")
    plt.tight_layout()

    fn = f"anomaly_{location_tag}_{event_date.date()}.png"
    fp = os.path.join(PLOT_DIR, fn)
    plt.savefig(fp)
    plt.close()
    return fp


def alert_pipeline(event_row, ctx_df, location_tag="lat:lon"):
    """
    event_row contains:
      - time
      - sst
      - iso_score
      - delta_from_mean
      - flag

    ctx_df = last ~30 days for plotting
    """

    event_time = event_row["time"]
    sst = float(event_row["sst"])
    delta = float(event_row["delta_from_mean"])

    # Decide warming vs cooling
    if delta > 0:
        direction = "Possible marine heat anomaly (warming)"
    else:
        direction = "Possible cold-water upwelling event (cooling)"

    # Build the readable alert string
    alert_msg = (
        f"Detected SST anomaly at {location_tag} on {event_time.date()}: "
        f"SST={sst:.2f}°C, deviation={delta:+.2f}°C from baseline. {direction}."
    )

    # Terminal output
    print_alert_terminal(alert_msg, level="ALERT")

    # Save plot
    fp = save_context_plot(ctx_df, event_time, location_tag)
    if fp:
        print_alert_terminal(f"Saved plot to {fp}", level="INFO")

    # Optional Slack alert
    slack_url = os.getenv("SLACK_WEBHOOK_URL", None)
    if not slack_url:
        print_alert_terminal("SLACK_WEBHOOK_URL not configured; skipping Slack.", level="WARN")
        return

    # If Slack is configured, send a simple message
    try:
        import requests
        requests.post(slack_url, json={"text": alert_msg})
    except Exception as e:
        print_alert_terminal(f"Slack send failed: {e}", level="WARN")
