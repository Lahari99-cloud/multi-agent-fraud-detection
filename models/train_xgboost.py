from __future__ import annotations
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

FEATURES = [
    "amount",
    "hour",
    "txn_count_5m",
    "txn_count_1h",
    "failed_attempts_1h",
    "new_device",
    "foreign_country",
    "merchant_novelty",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="models/xgboost_model.pkl")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    X = df[FEATURES]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)

    print(f"ROC-AUC: {auc:.4f}")

    joblib.dump(model, args.output)
    print(f"Saved model to {args.output}")


if __name__ == "__main__":
    main()