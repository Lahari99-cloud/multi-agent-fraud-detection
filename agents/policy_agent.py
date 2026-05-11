from __future__ import annotations

from pipeline.state import FraudState


def policy_agent(state: FraudState) -> FraudState:
    f = state["features"]
    rule_score = 0.0
    reason_codes = state.get("reason_codes", [])

    if f["amount_to_avg_ratio"] >= 8:
        rule_score += 0.25
        reason_codes.append("AMOUNT_DEVIATION")

    if f["distance_from_home_miles"] >= 750:
        rule_score += 0.20
        reason_codes.append("LOCATION_DEVIATION")

    if f["txn_count_5m"] >= 4 or f["txn_count_1h"] >= 10:
        rule_score += 0.20
        reason_codes.append("VELOCITY_RISK")

    if f["new_device"]:
        rule_score += 0.15
        reason_codes.append("NEW_DEVICE")

    if f["foreign_country"]:
        rule_score += 0.15
        reason_codes.append("FOREIGN_COUNTRY")

    if f["risky_category"]:
        rule_score += 0.10
        reason_codes.append("RISKY_MERCHANT_CATEGORY")

    if f["failed_attempts_1h"] >= 2:
        rule_score += 0.15
        reason_codes.append("FAILED_ATTEMPTS")

    rule_score = min(rule_score, 1.0)

    audit = state.get("audit_trail", []) + ["policy"]

    return {
        **state,
        "rule_score": rule_score,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "audit_trail": audit,
    }