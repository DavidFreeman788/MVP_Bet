from __future__ import annotations


def roi(total_profit: float, total_staked: float) -> float:
    return total_profit / total_staked if total_staked else 0.0


def yield_pct(total_profit: float, total_staked: float) -> float:
    return roi(total_profit, total_staked)
