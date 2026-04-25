from __future__ import annotations

import random


def simulate_best_of_3(p_set_a: float, n_simulations: int = 10000) -> dict:
    results = {"2:0": 0, "2:1": 0, "1:2": 0, "0:2": 0, "a_wins": 0, "games_total": []}
    for _ in range(n_simulations):
        a_sets = 0
        b_sets = 0
        games = 0
        while a_sets < 2 and b_sets < 2:
            a_won = random.random() < p_set_a
            if a_won:
                a_sets += 1
                games += random.randint(9, 13)
            else:
                b_sets += 1
                games += random.randint(9, 13)
        score = f"{a_sets}:{b_sets}"
        if score in results:
            results[score] += 1
        if a_sets > b_sets:
            results["a_wins"] += 1
        results["games_total"].append(games)

    return {
        "p_match_a": results["a_wins"] / n_simulations,
        "p_2_0": results["2:0"] / n_simulations,
        "p_2_1": results["2:1"] / n_simulations,
        "p_1_2": results["1:2"] / n_simulations,
        "p_0_2": results["0:2"] / n_simulations,
        "avg_total_games": sum(results["games_total"]) / n_simulations,
    }
