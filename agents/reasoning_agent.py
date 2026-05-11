from __future__ import annotations

import os
from typing import Any

from agents.schemas import FraudExplanation
from pipeline.state import FraudState


def _template_explanation(state: FraudState) -> FraudExplanation:
    reason_codes = state.get("reason_codes", [])
    risk_level = state.get("risk_level", "LOW")
    action = state.get("recommended_action", "APPROVE")
    risk_score = state.get("risk_score", 0.0)

    if reason_codes:
        factor_text = ", ".join(reason_codes)
    else:
        factor_text = "no material fraud indicators"

    return FraudExplanation(
        summary=(
            f"Risk level: {risk_level}. The decision was driven by {factor_text}. "
            f"Risk score: {risk_score}. Recommended action: {action}."
        ),
        key_risk_factors=list(reason_codes) or ["NORMAL_BEHAVIOR"],
        recommended_action=str(action),
    )


def _llm_explanation(state: FraudState) -> FraudExplanation:
    # Optional enterprise enhancement. The repo remains runnable without an API key.
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=0,
    )

    prompt = f"""
You are a senior financial fraud analyst.
Return a concise structured fraud explanation.

Transaction:
{state.get('transaction')}

Risk level: {state.get('risk_level')}
Reason codes: {state.get('reason_codes')}
Risk score: {state.get('risk_score')}
Recommended action: {state.get('recommended_action')}
"""

    return llm.with_structured_output(FraudExplanation).invoke(prompt)


def reasoning_agent(state: FraudState) -> FraudState:
    try:
        if os.getenv("OPENAI_API_KEY"):
            structured = _llm_explanation(state)
        else:
            structured = _template_explanation(state)
    except Exception:
        structured = _template_explanation(state)

    audit = state.get("audit_trail", []) + ["reasoning"]

    return {
        **state,
        "explanation": structured.summary,
        "llm_explanation": structured.model_dump(),
        "audit_trail": audit,
    }
