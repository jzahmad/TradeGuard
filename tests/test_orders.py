def test_create_order_requires_auth(client):
    response = client.post(
        "/api/orders", json={"symbol": "AAPL", "order_type": "BUY", "quantity": 1}
    )

    assert response.status_code == 401


def test_create_order_missing_fields(client, trader_headers):
    response = client.post("/api/orders", json={"symbol": "AAPL"}, headers=trader_headers)

    assert response.status_code == 400


def test_create_order_invalid_type(client, trader_headers, mock_prices):
    response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "HOLD", "quantity": 1},
        headers=trader_headers,
    )

    assert response.status_code == 400
    assert "BUY or SELL" in response.get_json()["error"]


def test_create_buy_order_insufficient_cash(client, trader_headers, mock_prices):
    response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 10},
        headers=trader_headers,
    )

    assert response.status_code == 400
    assert "Insufficient cash" in response.get_json()["error"]


def test_create_buy_order_success(client, trader_headers, fund_trader, mock_prices):
    response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 5},
        headers=trader_headers,
    )

    assert response.status_code == 201
    order = response.get_json()["order"]
    assert order["status"] == "PENDING"
    assert order["symbol"] == "AAPL"
    assert order["quantity"] == 5
    assert order["price"] == mock_prices["AAPL"]


def test_create_sell_order_insufficient_shares(client, trader_headers, mock_prices):
    response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "SELL", "quantity": 1},
        headers=trader_headers,
    )

    assert response.status_code == 400
    assert "Insufficient shares" in response.get_json()["error"]


def test_list_orders_only_shows_own_orders(client, trader_headers, fund_trader, mock_prices):
    client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 1},
        headers=trader_headers,
    )

    from tests.conftest import auth_header, login_user, register_user

    register_user(client, username="other_trader", password="password123")
    other_token = login_user(client, username="other_trader", password="password123")

    response = client.get("/api/orders", headers=auth_header(other_token))

    assert response.status_code == 200
    assert response.get_json()["orders"] == []


def test_get_single_order_not_owned_returns_404(client, trader_headers, fund_trader, mock_prices):
    create_response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 1},
        headers=trader_headers,
    )
    order_id = create_response.get_json()["order"]["id"]

    from tests.conftest import auth_header, login_user, register_user

    register_user(client, username="stranger", password="password123")
    stranger_token = login_user(client, username="stranger", password="password123")

    response = client.get(f"/api/orders/{order_id}", headers=auth_header(stranger_token))

    assert response.status_code == 404


def test_cancel_order_success(client, trader_headers, fund_trader, mock_prices):
    create_response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 1},
        headers=trader_headers,
    )
    order_id = create_response.get_json()["order"]["id"]

    response = client.delete(f"/api/orders/{order_id}", headers=trader_headers)

    assert response.status_code == 200
    assert response.get_json()["order"]["status"] == "CANCELLED"


def test_cancel_already_cancelled_order_fails(client, trader_headers, fund_trader, mock_prices):
    create_response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 1},
        headers=trader_headers,
    )
    order_id = create_response.get_json()["order"]["id"]
    client.delete(f"/api/orders/{order_id}", headers=trader_headers)

    response = client.delete(f"/api/orders/{order_id}", headers=trader_headers)

    assert response.status_code == 400


def test_cancel_nonexistent_order_returns_404(client, trader_headers):
    response = client.delete("/api/orders/999999", headers=trader_headers)

    assert response.status_code == 404
