from __future__ import annotations


def risk_level(confidence: float, data_quality: float) -> str:
    if data_quality < 0.6 or confidence < 0.55:
        return "high"
    if confidence < 0.7:
        return "medium"
    return "low"
