from pipeline.orchestrator import score_transaction


def test_high_risk_transaction_is_flagged():
    txn = {
        "transaction_id": "TXN-TEST-001",
        "customer_id": "CUST-1",
        "amount": 5000,
        "merchant": "Electronics Store",
        "merchant_category": "electronics",
        "lat": 36.1716,
        "lon": -115.1391,
        "home_lat": 38.9072,
        "home_lon": -77.0369,
        "hour": 2,
        "avg_amount_30d": 100,
        "txn_count_5m": 5,
        "txn_count_1h": 13,
        "new_device": True,
        "foreign_country": False,
        "merchant_novelty": True,
        "failed_attempts_1h": 3,
    }
    report = score_transaction(txn)
    assert report["flagged"] is True
    assert report["risk_level"] in {"HIGH", "CRITICAL"}
    assert "reasoning" in report["audit_trail"]
