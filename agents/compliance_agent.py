from __future__ import annotations

from datetime import datetime, timezone
from pipeline.state import FraudState


def compliance_agent(state: FraudState) -> FraudState:
    report = {
        "transaction_id": state["transaction"].get("transaction_id"),
        "decision_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "risk_level": state["risk_level"],
        "recommended_action": state["recommended_action"],
        "risk_score": state["risk_score"],
        "anomaly_score": state["anomaly_score"],
        "rule_score": state["rule_score"],
        "flagged": state["flagged"],
        "analyst_required": state.get("analyst_required", False),
        "analyst_notes": state.get("analyst_notes", ""),
        "reason_codes": state.get("reason_codes") or _reason_codes(state),
        "explanation": state.get("explanation", ""),
        "llm_explanation": state.get("llm_explanation", {}),
        "compliance_note": "Generated for fraud operations review; not an adverse credit decision notice.",
        "audit_trail": state.get("audit_trail", []) + ["compliance"],
    }
    return {**state, "compliance_report": report, "audit_trail": report["audit_trail"]}


def _reason_codes(state: FraudState) -> list[str]:
    f = state["features"]
    codes = []
    if f["amount_to_avg_ratio"] >= 3:
        codes.append("AMOUNT_DEVIATION")
    if f["distance_from_home_miles"] >= 500:
        codes.append("LOCATION_DEVIATION")
    if f["txn_count_5m"] >= 3 or f["txn_count_1h"] >= 8:
        codes.append("VELOCITY_RISK")
    if f["new_device"]:
        codes.append("NEW_DEVICE")
    if f["foreign_country"]:
        codes.append("FOREIGN_COUNTRY")
    if f["risky_category"]:
        codes.append("RISKY_MERCHANT_CATEGORY")
    return codes or ["NORMAL_BEHAVIOR"]
