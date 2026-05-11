from __future__ import annotations

from langgraph.graph import END, StateGraph

from agents.analyst_review_agent import analyst_review_agent
from agents.compliance_agent import compliance_agent
from agents.detection_agent import detection_agent
from agents.ingestion_agent import ingestion_agent
from agents.policy_agent import policy_agent
from agents.reasoning_agent import reasoning_agent
from agents.report_agent import report_agent
from agents.risk_scoring_agent import risk_scoring_agent
from pipeline.state import FraudState


def build_graph():
    graph = StateGraph(FraudState)

    graph.add_node("ingestion", ingestion_agent)
    graph.add_node("detection", detection_agent)
    graph.add_node("policy", policy_agent)
    graph.add_node("risk_scoring", risk_scoring_agent)
    graph.add_node("analyst_review", analyst_review_agent)
    graph.add_node("reasoning", reasoning_agent)
    graph.add_node("compliance", compliance_agent)
    graph.add_node("report", report_agent)

    graph.set_entry_point("ingestion")

    graph.add_edge("ingestion", "detection")
    graph.add_edge("detection", "policy")
    graph.add_edge("policy", "risk_scoring")
    graph.add_edge("risk_scoring", "analyst_review")
    graph.add_edge("analyst_review", "reasoning")
    graph.add_edge("reasoning", "compliance")
    graph.add_edge("compliance", "report")
    graph.add_edge("report", END)

    return graph.compile()


fraud_graph = build_graph()