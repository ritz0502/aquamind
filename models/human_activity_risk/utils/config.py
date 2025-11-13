# # Put your API keys here OR set environment variables and import them.
# # This file is loaded by the fetchers.
# # Replace the placeholder strings with actual keys.

# GEOAPIFY_KEY = "afe676f7b3bc46dd83bae4032172ed98"


# # AISStream does not require a key for the public geojson endpoint used here.
# # If you have a paid AIS provider, you can add credentials here.





# utils/config.py
DATA_DIR = "data/"
MODEL_PATH = "activity_risk_model.pkl"

# bbox used in synthetic generator and grid
GEO_BOUNDS = {
    "min_lat": 8.0,
    "max_lat": 22.6,
    "min_lon": 72.0,
    "max_lon": 88.4
}
