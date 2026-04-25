from __future__ import annotations

import pandas as pd


def load_odds_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
