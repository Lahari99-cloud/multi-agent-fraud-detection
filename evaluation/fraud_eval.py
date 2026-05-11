from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from pipeline.orchestrator import score_transaction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/transactions.csv")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", default="evaluation/reports/fraud_eval_report.json")
    args = parser.parse_args()

    df = pd.read_csv(args.input).head(args.limit)

    y_true: list[int] = []
    y_score: list[float] = []
    y_pred: list[int] = []

    for txn in df.to_dict(orient="records"):
        report = score_transaction(txn)

        y_true.append(int(txn.get("label_fraud", txn.get("is_fraud", 0))))
        y_score.append(float(report["risk_score"]))
        y_pred.append(int(report["flagged"]))

    metrics = {
        "records_evaluated": len(df),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }

    if len(set(y_true)) > 1:
        metrics["roc_auc"] = roc_auc_score(y_true, y_score)

    print(classification_report(y_true, y_pred, digits=3, zero_division=0))
    print(json.dumps(metrics, indent=2))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2))

    print(f"Saved evaluation report to {output_path}")


if __name__ == "__main__":
    main()