import requests


def test_stock_price_requires_auth(client):
    response = client.get("/api/stocks/AAPL")

    assert response.status_code == 401


def test_stock_price_success(client, trader_headers, mock_prices):
    response = client.get("/api/stocks/AAPL", headers=trader_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["symbol"] == "AAPL"
    assert body["current_price"] == mock_prices["AAPL"]


def test_stock_price_not_found(client, trader_headers, monkeypatch):
    def raise_value_error(symbol):
        raise ValueError(f"Finnhub returned no valid price for {symbol}")

    monkeypatch.setattr("app.controllers.stock_controller.get_stock_price", raise_value_error)

    response = client.get("/api/stocks/ZZZZ", headers=trader_headers)

    assert response.status_code == 404


def test_stock_price_upstream_failure(client, trader_headers, monkeypatch):
    def raise_request_exception(symbol):
        raise requests.RequestException("upstream down")

    monkeypatch.setattr("app.controllers.stock_controller.get_stock_price", raise_request_exception)

    response = client.get("/api/stocks/AAPL", headers=trader_headers)

    assert response.status_code == 502


def test_stock_search_requires_query(client, trader_headers):
    response = client.get("/api/stocks/search", headers=trader_headers)

    assert response.status_code == 400


def test_stock_search_success(client, trader_headers, mock_prices):
    response = client.get("/api/stocks/search?q=apple", headers=trader_headers)

    assert response.status_code == 200
    results = response.get_json()["results"]
    assert len(results) == 1
    assert results[0]["symbol"] == "AAPL"
