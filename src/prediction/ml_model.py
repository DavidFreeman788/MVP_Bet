from __future__ import annotations

from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

MODEL_PATH = Path("models/model.pkl")


FEATURE_COLUMNS = ["ranking_diff", "elo_diff", "surface_elo_diff", "form_10_diff", "fatigue_diff", "h2h_diff"]


def train_baseline(df):
    X = df[FEATURE_COLUMNS].fillna(0)
    y = df["target"]
    model = LogisticRegression(max_iter=500)
    model.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def predict_proba(features: dict) -> float | None:
    model = load_model()
    if model is None:
        return None
    row = np.array([[features.get(c, 0.0) for c in FEATURE_COLUMNS]])
    return float(model.predict_proba(row)[0][1])
