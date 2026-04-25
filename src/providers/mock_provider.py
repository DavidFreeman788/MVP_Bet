from __future__ import annotations

from datetime import datetime, timedelta
from src.providers.base import DataProvider


class MockProvider(DataProvider):
    def fetch_matches(self) -> list[dict]:
        now = datetime.utcnow()
        return [
            {
                "source_match_id": "mock-1",
                "tournament_name": "ATP Mock Open",
                "tour": "ATP",
                "round": "R32",
                "surface": "hard",
                "start_time": now + timedelta(hours=5),
                "player_a": "Carlos Alcaraz",
                "player_b": "Daniil Medvedev",
                "status": "scheduled",
                "data_quality_score": 0.82,
            }
        ]

    def fetch_odds(self) -> list[dict]:
        return [
            {
                "source_match_id": "mock-1",
                "bookmaker": "MockBook",
                "market_type": "match_winner",
                "selection": "Carlos Alcaraz",
                "line": None,
                "odds_decimal": 2.10,
            },
            {
                "source_match_id": "mock-1",
                "bookmaker": "MockBook",
                "market_type": "match_winner",
                "selection": "Daniil Medvedev",
                "line": None,
                "odds_decimal": 1.80,
            },
        ]
