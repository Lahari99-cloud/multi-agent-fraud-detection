from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_score() -> None:
    payload = {
        "transaction_id": "TXN-TEST-001",
        "amount": 9999.99,
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 200
    assert "risk_level" in response.json()