from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss
from src.prediction.ml_model import train_baseline, FEATURE_COLUMNS
from src.prediction.market_pricing import expected_value


def main():
    df = pd.DataFrame(
        [
            {"ranking_diff": -4, "elo_diff": 40, "surface_elo_diff": 35, "form_10_diff": 0.2, "fatigue_diff": -0.1, "h2h_diff": 0.1, "target": 1, "odds": 2.1},
            {"ranking_diff": 10, "elo_diff": -60, "surface_elo_diff": -50, "form_10_diff": -0.3, "fatigue_diff": 0.2, "h2h_diff": -0.1, "target": 0, "odds": 1.8},
            {"ranking_diff": -2, "elo_diff": 10, "surface_elo_diff": 8, "form_10_diff": 0.1, "fatigue_diff": -0.1, "h2h_diff": 0.02, "target": 1, "odds": 1.95},
            {"ranking_diff": 7, "elo_diff": -35, "surface_elo_diff": -25, "form_10_diff": -0.12, "fatigue_diff": 0.15, "h2h_diff": -0.04, "target": 0, "odds": 2.2},
        ]
    )
    model = train_baseline(df)
    proba = model.predict_proba(df[FEATURE_COLUMNS])[:, 1]
    pred = (proba >= 0.5).astype(int)

    metrics = {
        "accuracy": accuracy_score(df["target"], pred),
        "log_loss": log_loss(df["target"], proba),
        "brier_score": brier_score_loss(df["target"], proba),
    }

    df["ev"] = [expected_value(p, o) for p, o in zip(proba, df["odds"])]
    roi = df[df["ev"] > 0.03]["ev"].mean() if (df["ev"] > 0.03).any() else 0
    metrics["virtual_roi"] = float(roi)

    report = pd.DataFrame([metrics])
    Path("reports").mkdir(exist_ok=True)
    report.to_csv("reports/backtest_report.csv", index=False)
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
