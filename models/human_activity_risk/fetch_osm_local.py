import geopandas as gpd
from pyrosm import OSM
from shapely.geometry import Point
import os, requests, psutil, hashlib
from utils import cache_get, cache_set, make_key

DATA_DIR = "data/osm"
os.makedirs(DATA_DIR, exist_ok=True)

# Paths for datasets
PBF_PATH_INDIA = os.path.join(DATA_DIR, "india-latest.osm.pbf")
PBF_PATH_REGION = os.path.join(DATA_DIR, "south-india-latest.osm.pbf")
CACHE_POIS = os.path.join(DATA_DIR, "pois_cache.parquet")

# Define bounding box for South India coastline (min_lon, min_lat, max_lon, max_lat)
BBOX = [72.0, 8.0, 88.4, 22.6]

# Download URLs
URLS = {
    "india": "https://download.geofabrik.de/asia/india-latest.osm.pbf",
    "south_india": "https://download.geofabrik.de/asia/india/south-india-latest.osm.pbf"
}

def download_file(url, path):
    """Safe downloader with integrity check."""
    print(f"⬇️  Downloading {os.path.basename(path)} ...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, headers=headers, stream=True, timeout=120)
    total = int(r.headers.get("content-length", 0))
    downloaded = 0
    with open(path, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                print(f"\r  {downloaded/1e6:.1f}/{total/1e6:.1f} MB", end="")
    print(f"\n✅ Download complete: {path}")

    size_mb = os.path.getsize(path) / 1e6
    if size_mb < 100:
        raise ValueError(f"❌ File too small ({size_mb:.1f} MB). Download failed or truncated.")

    md5 = hashlib.md5(open(path, "rb").read(1024 * 1024)).hexdigest()
    print(f"🔍 File sanity check OK (MD5 head {md5[:8]})")

def ensure_pbf():
    """Ensure a working PBF exists."""
    if os.path.exists(PBF_PATH_REGION):
        print("🗺️  Using cached south-india-latest.osm.pbf")
        return PBF_PATH_REGION

    if os.path.exists(PBF_PATH_INDIA):
        size_gb = os.path.getsize(PBF_PATH_INDIA) / 1e9
        ram_gb = psutil.virtual_memory().total / 1e9
        if size_gb > 1.0 and ram_gb < 48:
            print(f"⚠️  india-latest.osm.pbf ({size_gb:.1f} GB) may exceed memory limit.")
            print("➡️  Downloading smaller south-india-latest.osm.pbf instead...")
            download_file(URLS["south_india"], PBF_PATH_REGION)
            return PBF_PATH_REGION
        else:
            print("🗺️  Using india-latest.osm.pbf")
            return PBF_PATH_INDIA
    else:
        print("⚠️  india-latest.osm.pbf not found — downloading smaller South India region.")
        download_file(URLS["south_india"], PBF_PATH_REGION)
        return PBF_PATH_REGION

def load_pois():
    """Load POIs from cache or extract from .pbf."""
    if os.path.exists(CACHE_POIS):
        print("⚡ Loading cached POIs from parquet...")
        return gpd.read_parquet(CACHE_POIS)

    pbf = ensure_pbf()
    print("🧭 Extracting POIs (first run only, may take a few minutes)...")

    # Pass bbox to the OSM instance (not to get_pois)
    osm = OSM(pbf, bounding_box=BBOX)

    pois = osm.get_pois(
        custom_filter={
            "harbour": True,
            "industrial": True,
            "man_made": ["works"],
            "tourism": ["hotel", "guest_house", "resort"]
        }
    )

    if pois is None or pois.empty:
        raise RuntimeError("❌ No POIs found. The .pbf file may be corrupted or incomplete.")

    pois = pois[["geometry", "harbour", "industrial", "man_made", "tourism"]].to_crs(epsg=4326)
    pois.to_parquet(CACHE_POIS)
    print(f"✅ Cached POIs ({len(pois)} records) for next runs.")
    return pois

# Global cache
POIS = load_pois()

def fetch_osm_counts(lat, lon, radius_m=5000):
    """Compute OSM object counts within radius."""
    key = make_key("osm_local", lat=lat, lon=lon, radius_m=radius_m)
    cached = cache_get(key)
    if cached:
        return cached

    center = Point(lon, lat)
    buffer_deg = radius_m / 111320.0
    area = center.buffer(buffer_deg)
    subset = POIS[POIS.intersects(area)]

    ports = len(subset[subset["harbour"].notnull()])
    industries = len(subset[(subset["industrial"].notnull()) | (subset["man_made"] == "works")])
    hotels = len(subset[subset["tourism"].notnull()])

    result = {
        "lat": lat,
        "lon": lon,
        "count_ports": int(ports),
        "count_industries": int(industries),
        "count_hotels": int(hotels)
    }

    cache_set(key, result)
    return result
