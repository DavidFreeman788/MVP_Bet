from __future__ import annotations


def is_value_bet(ev: float, edge: float, confidence: float, min_ev: float = 0.03, min_edge: float = 0.03, min_confidence: float = 0.60) -> bool:
    return ev > min_ev and edge > min_edge and confidence >= min_confidence
