from src.prediction.market_pricing import raw_implied_probability


def test_raw_implied_probability():
    assert abs(raw_implied_probability(2.0) - 0.5) < 1e-9
