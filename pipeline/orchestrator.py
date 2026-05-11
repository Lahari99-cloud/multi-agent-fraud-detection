from __future__ import annotations

from pipeline.graph import fraud_graph
from pipeline.state import FraudState


def score_transaction(transaction: dict) -> dict:
    initial_state: FraudState = {"transaction": transaction, "audit_trail": []}
    final_state = fraud_graph.invoke(initial_state)
    return final_state["compliance_report"]
