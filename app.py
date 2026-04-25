from __future__ import annotations

import json
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from sqlalchemy import select

from src.config import settings
from src.db import get_session
from src.models import Match, Odds, ModelPrediction, Bet, AppSetting, Tournament
from src.prediction.analytical_model import predict_match_probability
from src.prediction.ml_model import predict_proba
from src.prediction.market_pricing import edge, expected_value
from src.prediction.explanation import build_explanation
from src.prediction.risk import risk_level
from src.betting.bankroll import recommended_stake
from src.betting.value_finder import is_value_bet
from src.betting.bet_journal import roi, yield_pct

st.set_page_config(page_title="Tennis Betting Analyst MVP", layout="wide")


def get_setting(session, key, default):
    s = session.execute(select(AppSetting).where(AppSetting.key == key)).scalar_one_or_none()
    return s.value if s else default


def sidebar_page():
    return st.sidebar.radio("Навигация", ["Dashboard", "Matches", "Match Detail", "Bet Journal", "Analytics", "Settings"])


def load_matches_df(session):
    now = datetime.utcnow()
    horizon = now + timedelta(days=2)
    q = (
        select(Match.id, Match.start_time, Match.tour, Match.surface, Match.data_quality_score, Tournament.name.label("tournament"))
        .join(Tournament, Match.tournament_id == Tournament.id)
        .where(Match.start_time >= now, Match.start_time <= horizon)
    )
    rows = session.execute(q).all()
    return pd.DataFrame(rows, columns=["id", "start_time", "tour", "surface", "data_quality_score", "tournament"])


def render_dashboard(session):
    st.title("🎾 Tennis Betting Analyst MVP")
    bets = session.execute(select(Bet)).scalars().all()
    total_profit = sum(b.profit_loss for b in bets)
    total_staked = sum(b.stake for b in bets)
    current_bankroll = settings.default_bankroll + total_profit

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bankroll", f"{current_bankroll:,.2f}")
    col2.metric("ROI", f"{roi(total_profit, total_staked):.2%}")
    col3.metric("Yield", f"{yield_pct(total_profit, total_staked):.2%}")
    col4.metric("Ставок", len(bets))


def render_matches(session):
    st.header("Matches")
    df = load_matches_df(session)
    st.dataframe(df, use_container_width=True)


def render_match_detail(session):
    st.header("Match Detail")
    matches = session.execute(select(Match)).scalars().all()
    if not matches:
        st.info("Нет матчей. Запустите scripts/seed_mock_data.py")
        return
    selected = st.selectbox("Выберите матч", options=matches, format_func=lambda m: f"{m.id}: {m.player_a.full_name} vs {m.player_b.full_name}")

    odds = session.execute(select(Odds).where(Odds.match_id == selected.id, Odds.market_type == "match_winner")).scalars().all()
    if len(odds) < 2:
        st.warning("Нет полной линии match_winner")
        return

    features = {
        "ranking_diff": -4,
        "elo_diff": 40,
        "surface_elo_diff": 35,
        "form_10_diff": 0.2,
        "fatigue_diff": -0.1,
        "h2h_diff": 0.1,
        "data_quality_score": selected.data_quality_score,
    }
    analytical = predict_match_probability(features)
    ml_p = predict_proba(features)
    p_model = 0.4 * analytical["p_a"] + 0.6 * ml_p if ml_p is not None else analytical["p_a"]

    p_fair = odds[0].fair_probability if odds[0].selection == selected.player_a.full_name else odds[1].fair_probability
    odd_a = odds[0].odds_decimal if odds[0].selection == selected.player_a.full_name else odds[1].odds_decimal
    e = edge(p_model, p_fair)
    ev = expected_value(p_model, odd_a)
    risk = risk_level(analytical["confidence_score"], selected.data_quality_score)
    stake = recommended_stake(settings.default_bankroll, p_model, odd_a, settings.max_stake_percent, settings.kelly_multiplier)
    is_value = is_value_bet(ev, e, analytical["confidence_score"], settings.min_ev_threshold, settings.min_edge_threshold, settings.min_confidence_threshold)

    explanation = build_explanation(
        selected.player_a.full_name,
        selected.player_b.full_name,
        p_model,
        p_fair,
        analytical["factors"],
        analytical["risk_flags"],
        stake / settings.default_bankroll if settings.default_bankroll else 0,
    )

    st.write({
        "model_probability": round(p_model, 4),
        "fair_probability": round(p_fair, 4),
        "edge": round(e, 4),
        "ev": round(ev, 4),
        "confidence": round(analytical["confidence_score"], 4),
        "risk_level": risk,
        "recommended_stake": round(stake, 2),
        "is_value": is_value,
    })
    st.text(explanation)

    if st.button("Сохранить prediction"):
        pred = ModelPrediction(
            match_id=selected.id,
            model_version="v1-hybrid",
            market_type="match_winner",
            selection=selected.player_a.full_name,
            model_probability=p_model,
            confidence_score=analytical["confidence_score"],
            risk_level=risk,
            edge=e,
            ev=ev,
            recommended_stake=stake,
            explanation_json=json.dumps({"text": explanation}, ensure_ascii=False),
        )
        session.add(pred)
        session.commit()
        st.success("Prediction saved")


def render_bet_journal(session):
    st.header("Bet Journal")
    preds = session.execute(select(ModelPrediction)).scalars().all()
    if preds:
        pred = st.selectbox("Выберите prediction", options=preds, format_func=lambda p: f"{p.id} | match {p.match_id} | EV {p.ev:.2%}")
        if st.button("Сохранить ставку"):
            bankroll = settings.default_bankroll
            bet = Bet(
                match_id=pred.match_id,
                prediction_id=pred.id,
                bookmaker="MockBook",
                market_type=pred.market_type,
                selection=pred.selection,
                odds_decimal=2.1,
                stake=pred.recommended_stake,
                bankroll_before=bankroll,
                model_probability=pred.model_probability,
                fair_probability=pred.model_probability - pred.edge,
                edge=pred.edge,
                ev=pred.ev,
                status="planned",
            )
            session.add(bet)
            session.commit()
            st.success("Ставка сохранена")

    bets = session.execute(select(Bet)).scalars().all()
    if bets:
        df = pd.DataFrame([
            {"id": b.id, "match_id": b.match_id, "selection": b.selection, "odds": b.odds_decimal, "stake": b.stake, "status": b.status, "pnl": b.profit_loss}
            for b in bets
        ])
        st.dataframe(df, use_container_width=True)


def render_analytics(session):
    st.header("Analytics")
    bets = session.execute(select(Bet)).scalars().all()
    if not bets:
        st.info("Нет ставок")
        return
    df = pd.DataFrame([{"stake": b.stake, "pnl": b.profit_loss, "status": b.status} for b in bets])
    st.write({
        "profit_loss": float(df["pnl"].sum()),
        "roi": roi(df["pnl"].sum(), df["stake"].sum()),
        "winrate": float((df["pnl"] > 0).mean()),
        "avg_odds": 0,
    })


def render_settings(session):
    st.header("Settings")
    st.write("Текущие параметры из .env")
    st.json({
        "DEFAULT_BANKROLL": settings.default_bankroll,
        "MAX_STAKE_PERCENT": settings.max_stake_percent,
        "KELLY_MULTIPLIER": settings.kelly_multiplier,
        "MIN_EV_THRESHOLD": settings.min_ev_threshold,
        "MIN_EDGE_THRESHOLD": settings.min_edge_threshold,
        "MIN_CONFIDENCE_THRESHOLD": settings.min_confidence_threshold,
    })


page = sidebar_page()
session = get_session()

if page == "Dashboard":
    render_dashboard(session)
elif page == "Matches":
    render_matches(session)
elif page == "Match Detail":
    render_match_detail(session)
elif page == "Bet Journal":
    render_bet_journal(session)
elif page == "Analytics":
    render_analytics(session)
else:
    render_settings(session)
