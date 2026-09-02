import os

# Force a dedicated test database and deterministic secrets *before* app.config
# is ever imported, so the test suite never touches real dev/CI data and never
# depends on a real .env file being present (it won't be, in CI).
TEST_DB_NAME = "tradeguard_test"
os.environ["MYSQL_DATABASE"] = TEST_DB_NAME
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "3306")
os.environ.setdefault("MYSQL_USER", "root")
os.environ.setdefault("MYSQL_PASSWORD", "")
os.environ.setdefault("SECRET_KEY", "test-secret-key-0123456789abcdef")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key-0123456789abcdef")
os.environ.setdefault("FINNHUB_API_KEY", "test-finnhub-key")

import bcrypt
import pymysql
import pytest
from sqlalchemy import text

from app import create_app
from app.extensions import db as _db


def _ensure_database_exists():
    connection = pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}")
        connection.commit()
    finally:
        connection.close()


@pytest.fixture(scope="session")
def app():
    _ensure_database_exists()

    flask_app = create_app()
    flask_app.config.update(TESTING=True)

    with flask_app.app_context():
        _db.drop_all()
        _db.create_all()
        _db.session.remove()

    yield flask_app

    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Truncate every table before each test so tests never see each other's data."""
    with app.app_context():
        _db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        _db.session.commit()
        _db.session.remove()
    yield


@pytest.fixture
def mock_prices(monkeypatch):
    """Stub out every real Finnhub call so tests never hit the network."""
    prices = {"AAPL": 100.00, "MSFT": 200.00, "TSLA": 300.00}

    def fake_get_price(symbol):
        return prices.get(symbol.upper(), 50.00)

    def fake_search(query):
        return [{"symbol": "AAPL", "description": "Apple Inc", "type": "Common Stock"}]

    # Each of these modules did `from app.services.stock_service import ...`,
    # binding its own local name at import time - patching stock_service itself
    # would not affect those already-bound references, so patch every call site.
    monkeypatch.setattr("app.services.order_service.get_stock_price", fake_get_price)
    monkeypatch.setattr("app.services.stock_service.get_stock_price", fake_get_price)
    monkeypatch.setattr("app.services.stock_service.search_stocks", fake_search)
    monkeypatch.setattr("app.controllers.stock_controller.get_stock_price", fake_get_price)
    monkeypatch.setattr("app.controllers.stock_controller.search_stocks", fake_search)

    return prices


def register_user(client, username="trader1", password="password123", **overrides):
    payload = {
        "name": overrides.get("name", "Test Trader"),
        "username": username,
        "email": overrides.get("email", f"{username}@example.com"),
        "password": password,
    }
    return client.post("/api/auth/register", json=payload)


def login_user(client, username="trader1", password="password123"):
    response = client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )
    return response.get_json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def trader_token(client):
    register_user(client, username="trader1", password="password123")
    return login_user(client, username="trader1", password="password123")


@pytest.fixture
def trader_headers(trader_token):
    return auth_header(trader_token)


@pytest.fixture
def fund_trader(app, trader_token):
    """Give the logged-in trader enough cash to place BUY orders."""
    from app.models.user import User
    from app.models.portfolio import Portfolio

    with app.app_context():
        user = User.query.filter_by(username="trader1").first()
        portfolio = Portfolio.query.filter_by(user_id=user.id).first()
        portfolio.cash_balance = 100000
        _db.session.commit()
        return user.id


@pytest.fixture
def admin_headers(app, client):
    from app.models.user import User
    from app.models.portfolio import Portfolio

    with app.app_context():
        password_hash = bcrypt.hashpw(b"adminpass123", bcrypt.gensalt()).decode("utf-8")
        admin = User(
            name="Test Admin",
            username="admin1",
            email="admin1@example.com",
            password_hash=password_hash,
            role="ADMIN",
        )
        _db.session.add(admin)
        _db.session.flush()
        _db.session.add(Portfolio(user_id=admin.id, cash_balance=0))
        _db.session.commit()

    token = login_user(client, username="admin1", password="adminpass123")
    return auth_header(token)


__all__ = [
    "register_user",
    "login_user",
    "auth_header",
]
