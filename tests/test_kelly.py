from src.betting.bankroll import kelly_fraction, recommended_stake


def test_kelly_positive():
    kf = kelly_fraction(0.55, 2.1)
    assert kf > 0


def test_recommended_stake_capped():
    stake = recommended_stake(1000, 0.9, 3.0, max_stake_percent=0.02)
    assert stake <= 20
