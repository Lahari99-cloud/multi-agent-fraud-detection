from __future__ import annotations

import joblib
import numpy as np


class EnsembleScorer:
    def __init__(self) -> None:
        self.xgb_model = joblib.load("models/xgboost_model.pkl")

    def score(self, features: dict, anomaly_score: float, rule_score: float) -> float:
        xgb_features = np.array([
            [
                features["amount"],
                features["hour"],
                features["txn_count_5m"],
                features["txn_count_1h"],
                features["failed_attempts_1h"],
                int(features["new_device"]),
                int(features["foreign_country"]),
                int(features["merchant_novelty"]),
            ]
        ])

        xgb_score = self.xgb_model.predict_proba(xgb_features)[0][1]

        normalized_if = min(max(abs(anomaly_score), 0.0), 1.0)

        final_score = (
            0.4 * normalized_if +
            0.4 * xgb_score +
            0.2 * rule_score
        )

        return round(float(final_score), 4)