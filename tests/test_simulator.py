from src.prediction.simulator import simulate_best_of_3


def test_simulator_probabilities():
    out = simulate_best_of_3(0.6, n_simulations=1000)
    assert 0 <= out["p_match_a"] <= 1
    assert abs(out["p_2_0"] + out["p_2_1"] + out["p_1_2"] + out["p_0_2"] - 1) < 0.05
