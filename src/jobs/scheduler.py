from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler


def build_scheduler():
    scheduler = BackgroundScheduler()
    return scheduler
