from __future__ import annotations

from math import radians, sin, cos, asin, sqrt
from typing import Any

import pandas as pd

RISKY_CATEGORIES = {"electronics", "jewelry", "crypto", "gift_card", "wire_transfer"}


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 3958.8
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * radius * asin(sqrt(a))


def extract_features(txn: dict[str, Any]) -> dict[str, Any]:
    amount = float(txn.get("amount", 0.0))
    avg_amount_30d = max(float(txn.get("avg_amount_30d", 1.0)), 1.0)
    user_lat = float(txn.get("home_lat", txn.get("lat", 0.0)))
    user_lon = float(txn.get("home_lon", txn.get("lon", 0.0)))
    lat = float(txn.get("lat", user_lat))
    lon = float(txn.get("lon", user_lon))
    distance = haversine_miles(user_lat, user_lon, lat, lon)
    hour = int(txn.get("hour", 12))
    category = str(txn.get("merchant_category", "other")).lower()

    return {
        "amount": amount,
        "amount_to_avg_ratio": amount / avg_amount_30d,
        "distance_from_home_miles": distance,
        "txn_count_5m": int(txn.get("txn_count_5m", 0)),
        "txn_count_1h": int(txn.get("txn_count_1h", 0)),
        "new_device": int(bool(txn.get("new_device", False))),
        "foreign_country": int(bool(txn.get("foreign_country", False))),
        "risky_category": int(category in RISKY_CATEGORIES),
        "unusual_hour": int(hour < 5 or hour > 23),
        "merchant_novelty": int(bool(txn.get("merchant_novelty", False))),
        "failed_attempts_1h": int(txn.get("failed_attempts_1h", 0)),
    }


def features_to_frame(features: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([features])


FEATURE_COLUMNS = [
    "amount",
    "amount_to_avg_ratio",
    "distance_from_home_miles",
    "txn_count_5m",
    "txn_count_1h",
    "new_device",
    "foreign_country",
    "risky_category",
    "unusual_hour",
    "merchant_novelty",
    "failed_attempts_1h",
]
