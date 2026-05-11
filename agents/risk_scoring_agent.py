from __future__ import annotations

from pipeline.state import FraudState


def risk_scoring_agent(state: FraudState) -> FraudState:
    anomaly_component = min(
        abs(float(state.get("anomaly_score", 0.0))),
        1.0,
    )

    rule_component = min(
        float(state.get("rule_score", 0.0)),
        1.0,
    )

    f = state["features"]

    velocity_component = min(
        (f["txn_count_5m"] / 5) * 0.5
        + (f["txn_count_1h"] / 20) * 0.5,
        1.0,
    )

    merchant_novelty = 1.0 if f["merchant_novelty"] else 0.0

    behavior_component = min(
        (f["amount_to_avg_ratio"] / 12) * 0.7
        + merchant_novelty * 0.3,
        1.0,
    )

    risk_score = round(
        0.40 * anomaly_component
        + 0.30 * rule_component
        + 0.20 * velocity_component
        + 0.10 * behavior_component,
        4,
    )

    if risk_score >= 0.75:
        risk_level = "CRITICAL"
        action = "SOFT_DECLINE"

    elif risk_score >= 0.5:
        risk_level = "HIGH"
        action = "ANALYST_REVIEW"

    elif risk_score >= 0.3:
        risk_level = "MEDIUM"
        action = "STEP_UP_AUTH"

    else:
        risk_level = "LOW"
        action = "APPROVE"

    audit = state.get("audit_trail", []) + ["risk_scoring"]

    return {
        **state,
        "risk_score": risk_score,
        "flagged": risk_level in {"HIGH", "CRITICAL"},
        "risk_level": risk_level,
        "recommended_action": action,
        "audit_trail": audit,
    }