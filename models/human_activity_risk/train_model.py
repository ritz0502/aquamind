# # train_model.py
# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LinearRegression, Ridge, Lasso
# from sklearn.model_selection import GridSearchCV, GroupKFold
# from sklearn.metrics import mean_absolute_error, make_scorer
# from xgboost import XGBRegressor

# from utils import spatial_groups

# DATA_PATH = "data/osm_samples_joined.csv"
# MODEL_OUT = "models/best_pipeline.joblib"
# N_GROUPS = 6

# def load_data(path=DATA_PATH):
#     df = pd.read_csv(path)
#     df = df.dropna(subset=["count_ports","count_industries","count_hotels","activity_score","sat_label","lat","lon"])
#     for c in ["count_ports","count_industries","count_hotels","activity_score","sat_label","lat","lon"]:
#         df[c] = pd.to_numeric(df[c], errors="coerce")
#     df = df.dropna(subset=["sat_label"])
#     return df

# def build_and_search(df):
#     X = df[["count_ports","count_industries","count_hotels","activity_score"]].values
#     y = df["sat_label"].values
#     latlons = df[["lat","lon"]].values
#     groups = spatial_groups(latlons, n_groups=N_GROUPS)

#     pipelines = {
#         "linear": Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())]),
#         "ridge": Pipeline([("scaler", StandardScaler()), ("ridge", Ridge())]),
#         "lasso": Pipeline([("scaler", StandardScaler()), ("lasso", Lasso(max_iter=5000))]),
#         "xgb": Pipeline([("scaler", StandardScaler()), ("xgb", XGBRegressor(objective="reg:squarederror", verbosity=0, random_state=42))])
#     }

#     param_grids = {
#         "linear": {"lr__fit_intercept": [True]},
#         "ridge": {"ridge__alpha": [0.1, 1.0, 10.0]},
#         "lasso": {"lasso__alpha": [0.001, 0.01, 0.1]},
#         "xgb": {"xgb__n_estimators": [50, 100], "xgb__max_depth":[2,3,4], "xgb__learning_rate":[0.01,0.1]}
#     }

#     best = None
#     best_score = float("inf")

#     gkf = GroupKFold(n_splits=min(N_GROUPS, len(np.unique(groups))))

#     for name, pipe in pipelines.items():
#         print("Searching", name)
#         grid = GridSearchCV(pipe, param_grids[name],
#                             cv=gkf.split(X, y, groups=groups),
#                             scoring="neg_mean_absolute_error",
#                             n_jobs=1, verbose=1)
#         grid.fit(X, y)
#         mae = -grid.best_score_
#         print(f" Model {name} gives MAE = {mae:.4f} with params {grid.best_params_}")
#         if mae < best_score:
#             best_score = mae
#             best = (name, grid.best_estimator_, mae)

#     print("Best overall model:", best[0], "MAE:", best[2])
#     os.makedirs("models", exist_ok=True)
#     joblib.dump(best[1], MODEL_OUT)
#     print("Saved best pipeline to", MODEL_OUT)
#     return best

# if __name__ == "__main__":
#     df = load_data()
#     print("Loaded training data with", len(df), "rows")
#     build_and_search(df)








































# train_model.py
import os, joblib, numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, GroupKFold
from xgboost import XGBRegressor
from utils import spatial_groups

DATA="data/osm_samples_joined.csv";OUT="models/best_pipeline.joblib"

def load():
    df=pd.read_csv(DATA).dropna(subset=["sat_label"])
    return df

def train(df):
    X=df[["count_ports","count_industries","count_hotels","activity_score"]].values
    y=df["sat_label"].values
    g=spatial_groups(df[["lat","lon"]].values)
    cv=GroupKFold(n_splits=min(5,len(np.unique(g))))
    models={
      "lin":(Pipeline([("s",StandardScaler()),("m",LinearRegression())]),{"m__fit_intercept":[True]}),
      "ridge":(Pipeline([("s",StandardScaler()),("m",Ridge())]),{"m__alpha":[0.1,1,10]}),
      "xgb":(Pipeline([("s",StandardScaler()),("m",XGBRegressor(objective="reg:squarederror",verbosity=0))]),{"m__n_estimators":[50,100],"m__max_depth":[2,3,4]})
    }
    best,best_score=None,1e9
    for n,(pipe,grid) in models.items():
        gs=GridSearchCV(pipe,grid,cv=cv.split(X,y,g),scoring="neg_mean_absolute_error",verbose=1)
        gs.fit(X,y)
        mae=-gs.best_score_;print(n,"MAE",mae)
        if mae<best_score:best, best_score=gs.best_estimator_, mae
    os.makedirs("models",exist_ok=True)
    joblib.dump(best,OUT)
    print("✅ Saved",OUT)

if __name__=="__main__":
    df=load();train(df)
