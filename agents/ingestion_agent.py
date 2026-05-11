from __future__ import annotations

from feature_store.feature_engineering import extract_features
from pipeline.state import FraudState


def ingestion_agent(state: FraudState) -> FraudState:
    audit = state.get("audit_trail", []) + ["ingestion"]
    features = extract_features(state["transaction"])
    return {**state, "features": features, "audit_trail": audit}
