from __future__ import annotations

from src.providers.base import DataProvider


class ManualProvider(DataProvider):
    def fetch_matches(self) -> list[dict]:
        return []

    def fetch_odds(self) -> list[dict]:
        return []
