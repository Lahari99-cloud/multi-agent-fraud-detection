from __future__ import annotations

from pipeline.state import FraudState


def report_agent(state: FraudState) -> FraudState:
    audit = state.get("audit_trail", []) + ["report"]
    report = {**state["compliance_report"], "audit_trail": audit}
    return {**state, "compliance_report": report, "audit_trail": audit}
