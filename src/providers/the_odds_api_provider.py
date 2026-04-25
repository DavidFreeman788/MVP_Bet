from __future__ import annotations

import requests
from src.config import settings


class TheOddsApiProvider:
    base_url = "https://api.the-odds-api.com/v4/sports/tennis_atp_wta/odds"

    def fetch_match_winner_odds(self, regions: str = "eu") -> dict:
        if not settings.the_odds_api_key:
            return {"status": "missing_api_key", "data": []}
        response = requests.get(
            self.base_url,
            params={
                "apiKey": settings.the_odds_api_key,
                "regions": regions,
                "markets": "h2h",
            },
            timeout=20,
        )
        response.raise_for_status()
        return {"status": "ok", "data": response.json()}
