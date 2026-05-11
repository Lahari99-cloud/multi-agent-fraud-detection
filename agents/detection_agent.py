from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from feature_store.feature_engineering import FEATURE_COLUMNS, features_to_frame
from pipeline.state import FraudState

MODEL_PATH = Path("models/anomaly_model.pkl")


def train_model(input_csv: str = "data/transactions.csv", model_path: Path = MODEL_PATH) -> None:
    df = pd.read_csv(input_csv)
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns in training data: {missing}")

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", IsolationForest(n_estimators=200, contamination=0.06, random_state=42)),
    ])
    pipeline.fit(df[FEATURE_COLUMNS])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"Saved anomaly model to {model_path}")


def _load_model(model_path: Path = MODEL_PATH) -> Any | None:
    if not model_path.exists():
        return None
    return joblib.load(model_path)


def detection_agent(state: FraudState) -> FraudState:
    model = _load_model()
    feature_df = features_to_frame(state["features"])[FEATURE_COLUMNS]

    if model is None:
        # Safe deterministic fallback when user has not trained yet.
        ratio = min(state["features"]["amount_to_avg_ratio"] / 12, 1.0)
        distance = min(state["features"]["distance_from_home_miles"] / 2500, 1.0)
        velocity = min(state["features"]["txn_count_1h"] / 15, 1.0)
        anomaly_score = -1 * max(ratio, distance, velocity)
    else:
        raw_score = float(model.decision_function(feature_df)[0])
        anomaly_score = max(-1.0, min(0.0, raw_score)) if raw_score < 0 else -0.05

    audit = state.get("audit_trail", []) + ["detection"]
    return {**state, "anomaly_score": anomaly_score, "audit_trail": audit}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--input", default="data/transactions.csv")
    args = parser.parse_args()
    if args.train:
        train_model(args.input)
