from __future__ import annotations

import mlflow


class MLflowTracker:
    def __init__(self, experiment_name: str = "fraud-detection") -> None:
        mlflow.set_experiment(experiment_name)

    def log_metrics(self, metrics: dict) -> None:
        with mlflow.start_run():
            for key, value in metrics.items():
                mlflow.log_metric(key, value)