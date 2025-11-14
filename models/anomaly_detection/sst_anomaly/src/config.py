# config.py - parameters
from datetime import timedelta

# detection/window parameters
TRAIN_WINDOW_DAYS = 60            # days used to fit IsolationForest
RETRAIN_EVERY = 24               # hours between retrain (if running full pipeline)
Z_SCORE_THRESHOLD = None         # z-score threshold
DELTA_THRESHOLD_DEGC = 0.2     # absolute change threshold in °C (e.g., 1°C jump)
ISOF_ESTIMATORS = 100
ISOF_CONTAMINATION = 0.05       # expected fraction of outliers in training data
ISOF_RANDOM_STATE = 42

# data fetch defaults (if using NOAA ERDDAP subset)
DEFAULT_LAT = 12.0
DEFAULT_LON = 72.0
DEFAULT_START_DATE = None  # if None, code will use today - TRAIN_WINDOW_DAYS - 7
DEFAULT_END_DATE = None

# output paths
DATA_DIR = "../data"
OUTPUT_DIR = "../outputs"
PLOT_DIR = OUTPUT_DIR + "/plots"
