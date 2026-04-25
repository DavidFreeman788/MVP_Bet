from src.prediction.market_pricing import fair_probabilities, expected_value, edge


def test_fair_probabilities_sum_to_one():
    fair, margin = fair_probabilities([2.0, 2.0])
    assert abs(sum(fair) - 1.0) < 1e-9
    assert abs(margin) < 1e-9


def test_edge_and_ev():
    assert edge(0.55, 0.5) == 0.05
    assert round(expected_value(0.55, 2.1), 3) == 0.155
