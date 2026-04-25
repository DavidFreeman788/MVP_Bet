from __future__ import annotations

import math


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def predict_match_probability(features: dict) -> dict:
    rating_diff = features.get("ranking_diff", 0) * -0.01
    elo_diff = features.get("elo_diff", 0) * 0.003
    surface_elo_diff = features.get("surface_elo_diff", 0) * 0.002
    form_diff = features.get("form_10_diff", 0) * 0.15
    fatigue_diff = features.get("fatigue_diff", 0) * -0.1
    h2h_diff = features.get("h2h_diff", 0) * 0.08
    data_quality = features.get("data_quality_score", 0.7)

    score = rating_diff + elo_diff + surface_elo_diff + form_diff + fatigue_diff + h2h_diff
    p_a = _sigmoid(score)
    confidence = max(0.35, min(0.95, 0.55 + (abs(score) * 0.15)))

    if data_quality < 0.65:
        confidence *= 0.8

    factors = [
        f"elo_diff={elo_diff:.3f}",
        f"surface_elo_diff={surface_elo_diff:.3f}",
        f"form_diff={form_diff:.3f}",
    ]
    risk_flags = []
    if data_quality < 0.65:
        risk_flags.append("low_data_quality")

    return {
        "p_a": p_a,
        "p_b": 1 - p_a,
        "confidence_score": confidence,
        "factors": factors,
        "risk_flags": risk_flags,
    }
