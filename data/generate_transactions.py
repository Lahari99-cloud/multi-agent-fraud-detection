from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd
from faker import Faker

from feature_store.feature_engineering import extract_features

fake = Faker()
random.seed(42)
Faker.seed(42)

CITIES = [
    ("Washington", "US", 38.9072, -77.0369),
    ("New York", "US", 40.7128, -74.0060),
    ("Dallas", "US", 32.7767, -96.7970),
    ("San Francisco", "US", 37.7749, -122.4194),
    ("Las Vegas", "US", 36.1716, -115.1391),
    ("London", "UK", 51.5072, -0.1276),
    ("Mexico City", "MX", 19.4326, -99.1332),
]
CATEGORIES = ["grocery", "restaurant", "gas", "travel", "electronics", "jewelry", "gift_card", "crypto"]


def generate_transaction(i: int, fraud_rate: float) -> dict:
    home_city = random.choice(CITIES[:4])
    is_fraud = random.random() < fraud_rate
    city = random.choice(CITIES[4:] if is_fraud else CITIES[:5])
    category = random.choice(["electronics", "jewelry", "gift_card", "crypto"] if is_fraud else CATEGORIES[:5])
    avg_amount = round(random.uniform(35, 240), 2)
    amount = round(random.uniform(avg_amount * 4, avg_amount * 18), 2) if is_fraud else round(random.uniform(5, avg_amount * 2.2), 2)

    txn = {
        "transaction_id": f"TXN-20260511-{i:06d}",
        "customer_id": f"CUST-{random.randint(1, 1200):05d}",
        "amount": amount,
        "merchant": fake.company(),
        "merchant_category": category,
        "city": city[0],
        "country": city[1],
        "lat": city[2],
        "lon": city[3],
        "home_lat": home_city[2],
        "home_lon": home_city[3],
        "hour": random.choice([1, 2, 3, 23]) if is_fraud else random.randint(6, 22),
        "avg_amount_30d": avg_amount,
        "txn_count_5m": random.randint(3, 7) if is_fraud else random.randint(0, 2),
        "txn_count_1h": random.randint(8, 18) if is_fraud else random.randint(0, 6),
        "new_device": is_fraud or random.random() < 0.08,
        "foreign_country": city[1] != "US",
        "merchant_novelty": is_fraud or random.random() < 0.12,
        "failed_attempts_1h": random.randint(1, 4) if is_fraud else random.choice([0, 0, 0, 1]),
        "label_fraud": int(is_fraud),
    }
    txn.update(extract_features(txn))
    return txn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-transactions", type=int, default=10000)
    parser.add_argument("--fraud-rate", type=float, default=0.06)
    parser.add_argument("--output", default="data/transactions.csv")
    args = parser.parse_args()

    df = pd.DataFrame([generate_transaction(i, args.fraud_rate) for i in range(args.num_transactions)])
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Generated {len(df)} transactions at {args.output}")


if __name__ == "__main__":
    main()
