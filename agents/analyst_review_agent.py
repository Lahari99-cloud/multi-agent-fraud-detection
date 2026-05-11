from __future__ import annotations

from pipeline.state import FraudState


def analyst_review_agent(state: FraudState) -> FraudState:
    risk_level = state.get("risk_level", "LOW")

    if risk_level in {"HIGH", "CRITICAL"}:
        analyst_required = True
        analyst_notes = (
            "Escalated to fraud operations for manual review."
        )

    else:
        analyst_required = False
        analyst_notes = ""

    audit = state.get("audit_trail", []) + ["analyst_review"]

    return {
        **state,
        "analyst_required": analyst_required,
        "analyst_notes": analyst_notes,
        "audit_trail": audit,
    }