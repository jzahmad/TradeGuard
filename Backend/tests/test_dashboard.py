def test_dashboard_requires_auth(client):
    response = client.get("/api/dashboard")

    assert response.status_code == 401


def test_dashboard_new_user_starts_with_initial_balance(client, trader_headers):
    response = client.get("/api/dashboard", headers=trader_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["cash_balance"] == 10000.0
    assert body["holdings"] == []


def test_dashboard_reflects_approved_holding(client, trader_headers, admin_headers, fund_trader, mock_prices):
    create_response = client.post(
        "/api/orders",
        json={"symbol": "AAPL", "order_type": "BUY", "quantity": 10},
        headers=trader_headers,
    )
    order_id = create_response.get_json()["order"]["id"]

    approve_response = client.post(
        f"/api/admin/orders/{order_id}/approve", headers=admin_headers
    )
    assert approve_response.status_code == 200

    response = client.get("/api/dashboard", headers=trader_headers)
    body = response.get_json()

    assert body["cash_balance"] == 100000 - (mock_prices["AAPL"] * 10)
    assert len(body["holdings"]) == 1
    assert body["holdings"][0]["symbol"] == "AAPL"
    assert body["holdings"][0]["quantity"] == 10
    assert body["holdings"][0]["average_price"] == mock_prices["AAPL"]
