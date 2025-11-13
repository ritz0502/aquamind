import folium
from folium.plugins import HeatMap
from utils.recommendations import risk_badge, recommendation

def create_map(df, output="activity_map.html", center=[15.0,78.0], zoom_start=5):
    """
    df must contain columns: lat, lon, activity_score
    Creates heatmap + marker layer with badge + recommendation popups.
    """
    m = folium.Map(location=center, zoom_start=zoom_start)

    # Heatmap uses rows of [lat, lon, weight]
    heat_data = df[["lat", "lon", "activity_score"]].values.tolist()
    HeatMap(heat_data, radius=22, blur=15, max_zoom=6).add_to(m)

    # Markers with badges
    for _, row in df.iterrows():
        score = float(row["activity_score"])
        color = "green" if score < 30 else ("orange" if score < 70 else "red")
        popup_html = f"""
        <b>Location:</b> {row['lat']:.4f}, {row['lon']:.4f}<br>
        <b>Activity Score:</b> {score:.1f}<br>
        <b>Risk:</b> {risk_badge(score)}<br><br>
        <b>Recommendation:</b><br>{recommendation(score)}
        """
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=350)
        ).add_to(m)

    m.save(output)
    print(f"🗺️ Map saved → {output}")
