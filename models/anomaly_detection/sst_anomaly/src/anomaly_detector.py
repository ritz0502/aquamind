# anomaly_detector.py
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from joblib import dump, load

from .config import (
    ISOF_ESTIMATORS,
    ISOF_CONTAMINATION,
    ISOF_RANDOM_STATE,
    DELTA_THRESHOLD_DEGC  # z-score intentionally removed
)

MODEL_PATH = "../outputs/isof_model.joblib"


class SSTAnomalyDetector:
    def __init__(self, n_estimators=ISOF_ESTIMATORS, contamination=ISOF_CONTAMINATION, random_state=ISOF_RANDOM_STATE):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state
        )
        self.trained = False
        self.train_df_cache = None   # <-- needed for rolling mean

    def fit(self, df_train):
        X = df_train[['sst']].values.reshape(-1, 1)
        Xs = self.scaler.fit_transform(X)
        self.model.fit(Xs)
        
        # store for rolling mean logic
        self.train_df_cache = df_train.copy()
        
        self.trained = True
        dump((self.scaler, self.model), MODEL_PATH)
        return self

    def load(self, path=MODEL_PATH):
        sc, mdl = load(path)
        self.scaler = sc
        self.model = mdl
        self.trained = True
        return self

    def score(self, df):
        if not self.trained:
            raise RuntimeError("Model not trained")

        X = df[['sst']].values.reshape(-1, 1)
        Xs = self.scaler.transform(X)

        iso_score = self.model.decision_function(Xs)
        iso_anom = self.model.predict(Xs) == -1

        # rolling mean from training window
        rolling_mean = self.train_df_cache['sst'].mean()

        # deviation from expected temperature
        delta_from_mean = df['sst'].iloc[0] - rolling_mean

        out = df.copy()
        out['iso_score'] = iso_score
        out['iso_anom'] = iso_anom
        out['delta_from_mean'] = delta_from_mean

        # final anomaly rule: IF + deviation threshold
        out['flag'] = (out['iso_anom']) & (abs(delta_from_mean) > DELTA_THRESHOLD_DEGC)

        return out
