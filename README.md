# Multi-Agent Fraud Detection System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://langchain-ai.github.io/langgraph/)

Enterprise-grade multi-agent fraud decisioning system using LangGraph, anomaly detection, policy orchestration, and explainability.

> Core design principle: the LLM/explanation layer does **not** make the fraud decision. Fraud decisions are generated through ML anomaly scoring, statistical rules, and deterministic policy orchestration. The explanation layer turns those decisions into analyst-readable and audit-ready summaries.

---

## Architecture

```text
Transaction -> Ingestion Agent -> Detection Agent -> Policy Agent -> Risk Scoring Agent -> Reasoning Agent -> Compliance Agent -> Report Agent
```

### Agents

| Agent | Responsibility |
|---|---|
| Ingestion Agent | Feature extraction from raw transaction payloads |
| Detection Agent | Isolation Forest anomaly detection with deterministic fallback |
| Policy Agent | Fraud policy rules: velocity, new device, location, risky category |
| Risk Scoring Agent | Ensemble score and recommended action |
| Reasoning Agent | Plain-English explanation for analysts |
| Compliance Agent | Structured JSON report with reason codes and audit trail |
| Report Agent | Final response shaping |

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m data.generate_transactions --num-transactions 10000
python -m agents.detection_agent --train --input data/transactions.csv
python -m pipeline.run_pipeline --input data/transactions.csv --limit 20
uvicorn api.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Score a transaction:

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-20260511-0001",
    "amount": 4847.23,
    "merchant": "Electronics Store",
    "merchant_category": "electronics",
    "city": "Las Vegas",
    "country": "US",
    "lat": 36.1716,
    "lon": -115.1391,
    "home_lat": 38.9072,
    "home_lon": -77.0369,
    "hour": 2,
    "avg_amount_30d": 185.0,
    "txn_count_5m": 4,
    "txn_count_1h": 11,
    "new_device": true,
    "foreign_country": false,
    "merchant_novelty": true,
    "failed_attempts_1h": 2
  }'
```

---

## Makefile Commands

```bash
make install
make generate
make train
make run
make api
make test
make eval
```

---

## Sample Output

```json
{
  "transaction_id": "TXN-20260511-0001",
  "risk_level": "HIGH",
  "recommended_action": "ANALYST_REVIEW",
  "risk_score": 0.6812,
  "flagged": true,
  "reason_codes": ["AMOUNT_DEVIATION", "LOCATION_DEVIATION", "VELOCITY_RISK", "NEW_DEVICE", "RISKY_MERCHANT_CATEGORY"],
  "explanation": "Risk level: HIGH. The decision was driven by: amount is 26.2x above the customer's 30-day average; merchant location is 2089 miles from the customer's home region; transaction velocity is elevated in the recent time window; transaction originated from a new device. Recommended action: Analyst Review.",
  "audit_trail": ["ingestion", "detection", "policy", "risk_scoring", "reasoning", "compliance", "report"]
}
```

---

## Evaluation

```bash
python evaluation/fraud_eval.py --input data/transactions.csv --limit 1000
```

Reports:
- precision
- recall
- F1
- ROC-AUC

---

## Observability

Prometheus metrics are available at:

```text
http://127.0.0.1:8000/metrics
```

Tracked metrics:
- total fraud scoring requests
- fraud scoring latency

---

## Docker

```bash
docker compose up --build
```

---

## GitHub Publishing Steps

```bash
git init
git add .
git commit -m "Initial multi-agent fraud detection system"
git branch -M main
git remote add origin https://github.com/Lahari99-cloud/multi-agent-fraud-detection.git
git push -u origin main
```

---

## Roadmap

- Kafka / Redpanda streaming ingestion
- React analyst dashboard
- MLflow model registry
- LangSmith/OpenTelemetry tracing
- Human-in-the-loop feedback queue
- Graph-based fraud ring detection
- XGBoost/LightGBM ensemble model

---

Built by [Lahari Tadepalli](https://github.com/Lahari99-cloud).
