from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from __future__ import annotations

import pandas as pd


def main():
    try:
        df = pd.read_csv("data/historical_matches.csv")
        print(f"Imported {len(df)} rows")
    except FileNotFoundError:
        print("No data/historical_matches.csv found. Place historical file and rerun.")


if __name__ == "__main__":
    main()
