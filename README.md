# Tennis Betting Analyst MVP

Личное Streamlit-приложение для анализа предматчевых ставок ATP/WTA (одиночные матчи):
- список матчей на сегодня/завтра;
- импорт/хранение коэффициентов;
- расчёт implied/fair probability, маржи, edge, EV;
- гибридный прогноз (Analytical + ML baseline);
- Monte Carlo симуляция best-of-3;
- журнал ставок, bankroll, ROI/yield;
- детерминированное объяснение прогноза;
- Telegram-уведомления (если заданы токены).

## Быстрый запуск

```bash
cp .env.example .env
pip install -r requirements.txt
python scripts/init_db.py
python scripts/seed_mock_data.py
streamlit run app.py
```

## Docker (опционально)

```bash
docker compose up --build
```

## Скрипты

```bash
python scripts/init_db.py
python scripts/seed_mock_data.py
python scripts/import_historical_data.py
python scripts/train_model.py
python scripts/backtest.py
pytest
```

## CSV импорт

Используйте `src/providers/csv_provider.py` и подайте CSV с колонками:
`source_match_id,bookmaker,market_type,selection,line,odds_decimal`.

## Переменные окружения

См. `.env.example`:
- API keys: `THE_ODDS_API_KEY`, `API_TENNIS_KEY`, `BKSIGNAL_API_KEY`, `ODDSCORP_API_KEY`;
- Telegram: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`;
- банкролл/пороги: `DEFAULT_BANKROLL`, `MAX_STAKE_PERCENT`, `KELLY_MULTIPLIER`, `MIN_EV_THRESHOLD`, `MIN_EDGE_THRESHOLD`, `MIN_CONFIDENCE_THRESHOLD`.

## Ограничения MVP

- без автопроставления ставок;
- ML baseline минимальный;
- live-рынки не поддержаны;
- часть провайдеров сделана как заглушка.
