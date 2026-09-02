# TradeGuard Backend

Flask + MySQL API for trading and portfolio management.

## Run locally

```bash
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # fill in real values
python run.py
```

API runs at `http://127.0.0.1:5000`.

## Tests

```bash
cd Backend
pytest tests/ -v
```

Tests use an isolated `tradeguard_test` MySQL database (auto-created) and mock
all Finnhub calls, so they never touch real data or need a real API key.
