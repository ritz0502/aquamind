import folium
from folium.plugins import HeatMap
from utils.recommendations import risk_badge, recommendation
import os

def create_map(df, output="../frontend/public/heatmaps/activity_map.html",
               center=[15.0, 78.0], zoom_start=5):

    # Ensure folder exists
    os.makedirs(os.path.dirname(output), exist_ok=True)

    # Dark themed map
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="CartoDB dark_matter"
    )

    # Heatmap
    heat_data = df[['lat', 'lon', 'activity_score']].values.tolist()
    HeatMap(
        heat_data,
        radius=26,
        blur=20,
        min_opacity=0.35
    ).add_to(m)

    # Nice popup CSS
    popup_css = """
    <style>
        .popup-card {
            background: rgba(15, 20, 28, 0.95);
            padding: 12px;
            border-radius: 12px;
            color: #d2f3ff;
            font-family: Poppins, sans-serif;
            width: 240px;
            box-shadow: 0 0 12px rgba(0,180,255,0.35);
        }
        .risk-badge {
            padding: 4px 8px;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 8px;
            display: inline-block;
        }
        .low { background:#0f5132; color:#d1f7e1; }
        .mod { background:#664d03; color:#fff5cc; }
        .high { background:#842029; color:#ffd0d6; }
    </style>
    """

    # Add markers with popups
    for _, row in df.iterrows():

        score = float(row["activity_score"])
        rec = recommendation(score).replace("\n", "<br>")
        badge = risk_badge(score)

        if score < 30:
            badge_class = "low"; color = "green"
        elif score < 70:
            badge_class = "mod"; color = "orange"
        else:
            badge_class = "high"; color = "red"

        popup_html = f"""
            {popup_css}
            <div class="popup-card">
                <b>📍 {row['lat']:.4f}, {row['lon']:.4f}</b><br><br>
                <b>Activity Score:</b> {score:.2f}<br>
                <span class="risk-badge {badge_class}">{badge}</span><br><br>
                <b>Recommendation:</b><br>{rec}
            </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.9
        ).add_child(folium.Popup(popup_html)).add_to(m)

    # Save HTML
    m.save(output)
    print("🗺️ Heatmap saved at:", output)
