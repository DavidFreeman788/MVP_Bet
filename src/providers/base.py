from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DataProvider(ABC):
    @abstractmethod
    def fetch_matches(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_odds(self) -> list[dict[str, Any]]:
        raise NotImplementedError
