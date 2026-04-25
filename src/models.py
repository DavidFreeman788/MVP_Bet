from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from src.db import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    source_player_id = Column(String, index=True)
    full_name = Column(String, nullable=False)
    normalized_name = Column(String, index=True)
    gender = Column(String)
    country = Column(String)
    birth_date = Column(Date)
    hand = Column(String)
    height_cm = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    source_tournament_id = Column(String, index=True)
    name = Column(String, nullable=False)
    tour = Column(String, index=True)
    level = Column(String)
    surface = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    source_match_id = Column(String, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tour = Column(String, index=True)
    round = Column(String)
    surface = Column(String)
    start_time = Column(DateTime)
    player_a_id = Column(Integer, ForeignKey("players.id"))
    player_b_id = Column(Integer, ForeignKey("players.id"))
    status = Column(String, default="scheduled")
    winner_player_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    score_raw = Column(String)
    best_of = Column(Integer, default=3)
    data_quality_score = Column(Float, default=0.7)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tournament = relationship("Tournament")
    player_a = relationship("Player", foreign_keys=[player_a_id])
    player_b = relationship("Player", foreign_keys=[player_b_id])


class Odds(Base):
    __tablename__ = "odds"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True)
    bookmaker = Column(String)
    market_type = Column(String)
    selection = Column(String)
    line = Column(String)
    odds_decimal = Column(Float)
    raw_implied_probability = Column(Float)
    fair_probability = Column(Float)
    market_margin = Column(Float)
    source = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class PlayerStatsSnapshot(Base):
    __tablename__ = "player_stats_snapshot"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    snapshot_date = Column(Date, default=date.today)
    surface = Column(String)
    ranking = Column(Integer)
    ranking_points = Column(Integer)
    elo_overall = Column(Float)
    elo_surface = Column(Float)
    matches_5 = Column(Integer)
    wins_5 = Column(Integer)
    matches_10 = Column(Integer)
    wins_10 = Column(Integer)
    matches_52w = Column(Integer)
    wins_52w = Column(Integer)
    surface_matches_52w = Column(Integer)
    surface_wins_52w = Column(Integer)
    hold_pct = Column(Float)
    break_pct = Column(Float)
    serve_points_won_pct = Column(Float)
    return_points_won_pct = Column(Float)
    tie_break_win_pct = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class ModelPrediction(Base):
    __tablename__ = "model_predictions"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True)
    model_version = Column(String)
    market_type = Column(String)
    selection = Column(String)
    line = Column(String)
    model_probability = Column(Float)
    confidence_score = Column(Float)
    risk_level = Column(String)
    edge = Column(Float)
    ev = Column(Float)
    recommended_stake = Column(Float)
    explanation_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True)
    prediction_id = Column(Integer, ForeignKey("model_predictions.id"), nullable=True)
    bookmaker = Column(String)
    market_type = Column(String)
    selection = Column(String)
    line = Column(String)
    odds_decimal = Column(Float)
    stake = Column(Float)
    bankroll_before = Column(Float)
    model_probability = Column(Float)
    fair_probability = Column(Float)
    edge = Column(Float)
    ev = Column(Float)
    status = Column(String, default="planned")
    profit_loss = Column(Float, default=0.0)
    placed_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime, nullable=True)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BankrollEvent(Base):
    __tablename__ = "bankroll_events"
    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    amount = Column(Float)
    bankroll_after = Column(Float)
    related_bet_id = Column(Integer, ForeignKey("bets.id"), nullable=True)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AppSetting(Base):
    __tablename__ = "app_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
