from __future__ import annotations

import requests
from src.config import settings


def send_message(text: str) -> dict:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return {"status": "disabled"}
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    r = requests.post(url, data={"chat_id": settings.telegram_chat_id, "text": text}, timeout=20)
    return {"status": "ok" if r.ok else "error", "code": r.status_code}
