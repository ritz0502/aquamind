import folium
from folium.plugins import HeatMap
import os

def create_map(lat, lon, activity_intensity=50):

    print("\n======================")
    print(" HEATMAP DEBUG OUTPUT ")
    print("======================\n")

    # Where is this file located?
    print("heatmap.py location:", os.path.dirname(__file__))

    # Move up 3 levels → project root
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    print("project_root:", project_root)

    # backend folder location
    backend_dir = os.path.join(project_root, "backend")
    print("backend_dir:", backend_dir)

    # final heatmaps folder
    heatmap_dir = os.path.join(backend_dir, "heatmaps")
    print("heatmap_dir:", heatmap_dir)

    # Create folder if missing
    os.makedirs(heatmap_dir, exist_ok=True)

    # Final heatmap path
    output_path = os.path.join(heatmap_dir, "activity_map.html")
    print("FINAL OUTPUT PATH:", output_path)

    # ----------------------------
    # Generate map
    # ----------------------------
    m = folium.Map(location=[lat, lon], zoom_start=10, tiles=None)

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© OpenStreetMap",
        control=False
    ).add_to(m)

    folium.CircleMarker([lat, lon], radius=10, color="red", fill=True).add_to(m)
    HeatMap([[lat, lon, activity_intensity]]).add_to(m)

    html = m.get_root().render()

    html = html.replace(
        "</head>",
        """
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
        </head>
        """
    )

    # Write file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("✔ File written successfully.")
    except Exception as e:
        print("❌ Failed to write file:", e)

    # Verify existence
    if os.path.exists(output_path):
        print("✔ File EXISTS after writing.")
    else:
        print("❌ File DOES NOT EXIST after writing!")

    print("\n======================\n")

    return "/heatmaps/activity_map.html"
