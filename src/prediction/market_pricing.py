from __future__ import annotations


def raw_implied_probability(decimal_odds: float) -> float:
    if decimal_odds <= 1:
        raise ValueError("odds must be > 1")
    return 1.0 / decimal_odds


def fair_probabilities(odds: list[float]) -> tuple[list[float], float]:
    implied = [raw_implied_probability(o) for o in odds]
    total = sum(implied)
    fair = [p / total for p in implied]
    margin = total - 1
    return fair, margin


def edge(model_probability: float, fair_probability: float) -> float:
    return model_probability - fair_probability


def expected_value(model_probability: float, decimal_odds: float) -> float:
    return model_probability * decimal_odds - 1
