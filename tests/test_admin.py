def _create_pending_order(client, trader_headers, symbol="AAPL", quantity=5, order_type="BUY"):
    response = client.post(
        "/api/orders",
        json={"symbol": symbol, "order_type": order_type, "quantity": quantity},
        headers=trader_headers,
    )
    return response.get_json()["order"]["id"]


def test_trader_forbidden_from_admin_routes(client, trader_headers, fund_trader, mock_prices):
    order_id = _create_pending_order(client, trader_headers)

    assert client.get("/api/admin/orders", headers=trader_headers).status_code == 403
    assert client.post(f"/api/admin/orders/{order_id}/approve", headers=trader_headers).status_code == 403
    assert client.post(f"/api/admin/orders/{order_id}/reject", headers=trader_headers).status_code == 403
    assert client.post(f"/api/admin/orders/{order_id}/flag", headers=trader_headers).status_code == 403


def test_admin_routes_require_auth(client):
    response = client.get("/api/admin/orders")

    assert response.status_code == 401


def test_admin_lists_all_orders(client, trader_headers, admin_headers, fund_trader, mock_prices):
    _create_pending_order(client, trader_headers)

    response = client.get("/api/admin/orders", headers=admin_headers)

    assert response.status_code == 200
    assert len(response.get_json()["orders"]) == 1


def test_admin_approve_buy_order_updates_cash_and_holdings(
    client, trader_headers, admin_headers, fund_trader, mock_prices
):
    order_id = _create_pending_order(client, trader_headers, symbol="AAPL", quantity=5)

    response = client.post(f"/api/admin/orders/{order_id}/approve", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["order"]["status"] == "APPROVED"

    dashboard = client.get("/api/dashboard", headers=trader_headers).get_json()
    assert dashboard["cash_balance"] == 100000 - (mock_prices["AAPL"] * 5)
    assert dashboard["holdings"][0]["quantity"] == 5


def test_admin_reject_order(client, trader_headers, admin_headers, fund_trader, mock_prices):
    order_id = _create_pending_order(client, trader_headers)

    response = client.post(f"/api/admin/orders/{order_id}/reject", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["order"]["status"] == "REJECTED"


def test_admin_flag_order(client, trader_headers, admin_headers, fund_trader, mock_prices):
    order_id = _create_pending_order(client, trader_headers)

    response = client.post(f"/api/admin/orders/{order_id}/flag", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["order"]["status"] == "FLAGGED"


def test_admin_cannot_approve_non_pending_order(client, trader_headers, admin_headers, fund_trader, mock_prices):
    order_id = _create_pending_order(client, trader_headers)
    client.post(f"/api/admin/orders/{order_id}/reject", headers=admin_headers)

    response = client.post(f"/api/admin/orders/{order_id}/approve", headers=admin_headers)

    assert response.status_code == 400
