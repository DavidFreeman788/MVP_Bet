from __future__ import annotations


def build_match_features(match_row: dict) -> dict:
    return {
        "ranking_diff": match_row.get("ranking_diff", 0),
        "elo_diff": match_row.get("elo_diff", 0),
        "surface_elo_diff": match_row.get("surface_elo_diff", 0),
        "form_10_diff": match_row.get("form_10_diff", 0),
        "fatigue_diff": match_row.get("fatigue_diff", 0),
        "h2h_diff": match_row.get("h2h_diff", 0),
        "data_quality_score": match_row.get("data_quality_score", 0.7),
    }
