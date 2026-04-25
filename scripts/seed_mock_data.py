from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from datetime import datetime, timedelta
from src.db import get_session
from src.models import Player, Tournament, Match, Odds
from src.prediction.market_pricing import raw_implied_probability, fair_probabilities


def main():
    session = get_session()
    p1 = Player(full_name="Carlos Alcaraz", normalized_name="carlos alcaraz", gender="M", country="ESP")
    p2 = Player(full_name="Daniil Medvedev", normalized_name="daniil medvedev", gender="M", country="RUS")
    session.add_all([p1, p2])
    session.flush()

    t = Tournament(name="ATP Mock Open", tour="ATP", level="250", surface="hard", location="Doha")
    session.add(t)
    session.flush()

    m = Match(
        source_match_id="mock-1",
        tournament_id=t.id,
        tour="ATP",
        round="R32",
        surface="hard",
        start_time=datetime.utcnow() + timedelta(hours=6),
        player_a_id=p1.id,
        player_b_id=p2.id,
        status="scheduled",
        data_quality_score=0.82,
        best_of=3,
    )
    session.add(m)
    session.flush()

    odds = [2.10, 1.80]
    fair, margin = fair_probabilities(odds)
    o1 = Odds(match_id=m.id, bookmaker="MockBook", market_type="match_winner", selection=p1.full_name, odds_decimal=odds[0], raw_implied_probability=raw_implied_probability(odds[0]), fair_probability=fair[0], market_margin=margin, source="mock")
    o2 = Odds(match_id=m.id, bookmaker="MockBook", market_type="match_winner", selection=p2.full_name, odds_decimal=odds[1], raw_implied_probability=raw_implied_probability(odds[1]), fair_probability=fair[1], market_margin=margin, source="mock")
    session.add_all([o1, o2])
    session.commit()
    print("Seeded mock data")


if __name__ == "__main__":
    main()
