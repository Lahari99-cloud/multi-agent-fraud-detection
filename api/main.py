from __future__ import annotations
from fastapi import WebSocket
import asyncio
import random
from typing import Any
import time

from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from pipeline.orchestrator import score_transaction


app = FastAPI(
    title="Multi-Agent Fraud Detection API",
    version="1.0.0",
    description="LangGraph-based fraud decisioning with ML anomaly detection and explainability.",
)

REQUESTS = Counter("fraud_requests_total", "Total fraud scoring requests")
FLAGGED = Counter("fraud_flagged_total", "Total flagged transactions")
LATENCY = Histogram("fraud_request_latency_seconds", "Fraud scoring latency")

ANALYST_QUEUE: list[dict[str, Any]] = []


class TransactionRequest(BaseModel):
    transaction_id: str = Field(..., examples=["TXN-20260511-0001"])
    customer_id: str = "CUST-001"
    amount: float = 4847.23
    merchant: str = "Electronics Store"
    merchant_category: str = "electronics"
    city: str = "Las Vegas"
    country: str = "US"
    lat: float = 36.1716
    lon: float = -115.1391
    home_lat: float = 38.9072
    home_lon: float = -77.0369
    hour: int = 2
    avg_amount_30d: float = 185.0
    txn_count_5m: int = 4
    txn_count_1h: int = 11
    new_device: bool = True
    foreign_country: bool = False
    merchant_novelty: bool = True
    failed_attempts_1h: int = 2


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "multi-agent-fraud-detection",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "analyst_queue": "/analyst/queue",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/score")
def score(request: TransactionRequest) -> dict[str, Any]:
    REQUESTS.inc()
    start = time.perf_counter()

    try:
        result = score_transaction(request.model_dump())

        if result.get("flagged") is True:
            FLAGGED.inc()

        if result.get("analyst_required") is True:
            ANALYST_QUEUE.append(result)

        return result

    finally:
        LATENCY.observe(time.perf_counter() - start)


@app.get("/analyst/queue")
def analyst_queue() -> list[dict[str, Any]]:
    return ANALYST_QUEUE


@app.delete("/analyst/queue")
def clear_analyst_queue() -> dict[str, Any]:
    cleared = len(ANALYST_QUEUE)
    ANALYST_QUEUE.clear()
    return {"status": "cleared", "cleared_cases": cleared}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.websocket("/ws/fraud-stream")
async def fraud_stream(websocket: WebSocket):
    await websocket.accept()

    while True:
        event = {
            "transaction_id": f"TXN-LIVE-{random.randint(1000,9999)}",
            "risk_level": random.choice(
                ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            ),
            "risk_score": round(random.uniform(0.1, 0.99), 3),
            "recommended_action": random.choice(
                [
                    "APPROVE",
                    "STEP_UP_AUTH",
                    "ANALYST_REVIEW",
                    "SOFT_DECLINE"
                ]
            ),
        }

        await websocket.send_json(event)

        await asyncio.sleep(2)
