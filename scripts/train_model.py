from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
import pandas as pd
from src.prediction.ml_model import train_baseline


def main():
    features_path = Path("features.csv")
    if features_path.exists():
        df = pd.read_csv(features_path)
    else:
        df = pd.DataFrame(
            [
                {"ranking_diff": -4, "elo_diff": 40, "surface_elo_diff": 35, "form_10_diff": 0.2, "fatigue_diff": -0.1, "h2h_diff": 0.1, "target": 1},
                {"ranking_diff": 10, "elo_diff": -60, "surface_elo_diff": -50, "form_10_diff": -0.3, "fatigue_diff": 0.2, "h2h_diff": -0.1, "target": 0},
                {"ranking_diff": 2, "elo_diff": -10, "surface_elo_diff": -5, "form_10_diff": -0.05, "fatigue_diff": 0.1, "h2h_diff": -0.05, "target": 0},
                {"ranking_diff": -8, "elo_diff": 70, "surface_elo_diff": 60, "form_10_diff": 0.25, "fatigue_diff": -0.2, "h2h_diff": 0.2, "target": 1},
            ]
        )
    train_baseline(df)
    print("Model trained and saved to models/model.pkl")


if __name__ == "__main__":
    main()
