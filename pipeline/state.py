from __future__ import annotations

from typing import Any, Literal, TypedDict

RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
Action = Literal["APPROVE", "STEP_UP_AUTH", "ANALYST_REVIEW", "SOFT_DECLINE"]


class FraudState(TypedDict, total=False):
    transaction: dict[str, Any]
    features: dict[str, Any]
    anomaly_score: float
    rule_score: float
    risk_score: float
    flagged: bool
    risk_level: RiskLevel
    recommended_action: Action
    reason_codes: list[str]
    explanation: str
    llm_explanation: dict[str, Any]
    analyst_required: bool
    analyst_notes: str
    feedback_label: str
    compliance_report: dict[str, Any]
    audit_trail: list[str]
