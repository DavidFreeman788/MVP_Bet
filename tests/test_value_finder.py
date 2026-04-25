from src.betting.value_finder import is_value_bet


def test_value_bet_thresholds():
    assert is_value_bet(0.05, 0.04, 0.7)
    assert not is_value_bet(0.01, 0.04, 0.7)
