from __future__ import annotations


def kelly_fraction(p: float, odds: float) -> float:
    return ((odds - 1) * p - (1 - p)) / (odds - 1)


def recommended_stake(bankroll: float, p: float, odds: float, max_stake_percent: float = 0.02, kelly_multiplier: float = 0.25) -> float:
    kf = max(0.0, kelly_fraction(p, odds))
    fraction = min(kf * kelly_multiplier, max_stake_percent)
    return bankroll * fraction
