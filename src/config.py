from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///tennis_betting.db")
    the_odds_api_key: str = os.getenv("THE_ODDS_API_KEY", "")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    default_bankroll: float = float(os.getenv("DEFAULT_BANKROLL", "100000"))
    max_stake_percent: float = float(os.getenv("MAX_STAKE_PERCENT", "0.02"))
    kelly_multiplier: float = float(os.getenv("KELLY_MULTIPLIER", "0.25"))
    min_ev_threshold: float = float(os.getenv("MIN_EV_THRESHOLD", "0.03"))
    min_edge_threshold: float = float(os.getenv("MIN_EDGE_THRESHOLD", "0.03"))
    min_confidence_threshold: float = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.60"))


settings = Settings()
