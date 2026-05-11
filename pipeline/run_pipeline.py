from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from rich import print

from pipeline.orchestrator import score_transaction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/transactions.csv")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", default="reports/fraud_reports.jsonl")
    args = parser.parse_args()

    df = pd.read_csv(args.input).head(args.limit)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    flagged = 0
    with out.open("w", encoding="utf-8") as f:
        for txn in df.to_dict(orient="records"):
            report = score_transaction(txn)
            flagged += int(report["flagged"])
            f.write(json.dumps(report) + "\n")

    print(f"Processed {len(df)} transactions. Flagged={flagged}. Output={out}")


if __name__ == "__main__":
    main()
