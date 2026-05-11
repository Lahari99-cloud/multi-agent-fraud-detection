from pydantic import BaseModel
class FraudExplanation(BaseModel):
    summary: str
    key_risk_factors: list[str]
    recommended_action: str