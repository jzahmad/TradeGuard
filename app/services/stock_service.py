import requests
from flask import current_app

from app.extensions import db
from app.models.stock import Stock

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

def get_stock_price(symbol):
    api_key = current_app.config.get("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError("FINNHUB_API_KEY is not configured")

    response = requests.get(
        f"{FINNHUB_BASE_URL}/quote",
        params={
            "symbol": symbol.upper(),
            "token": api_key,
        },
        timeout=10,
    )

    print("FINNHUB STATUS:", response.status_code)
    print("FINNHUB RESPONSE:", response.text)

    response.raise_for_status()

    data = response.json()
    price = data.get("c")

    if price is None or price <= 0:
        raise RuntimeError(
            f"Finnhub returned no valid price for {symbol}: {data}"
        )

    return price


def search_stocks(query):
    api_key = current_app.config.get("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError("FINNHUB_API_KEY is not configured")

    response = requests.get(
        f"{FINNHUB_BASE_URL}/search",
        params={
            "q": query,
            "token": api_key,
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()
    results = []

    for result in data.get("result", []):
        if result.get("type") != "Common Stock":
            continue

        symbol = result.get("symbol")
        description = result.get("description")

        if not symbol:
            continue

        results.append({
            "symbol": symbol,
            "description": description,
            "type": result.get("type"),
        })

    return results


def get_or_create_stock(symbol, company_name=None):
    symbol = symbol.upper()

    stock = Stock.query.filter_by(symbol=symbol).first()

    if stock:
        return stock

    price = get_stock_price(symbol)

    stock = Stock(
        symbol=symbol,
        company_name=company_name or symbol,
        current_price=price,
    )

    db.session.add(stock)
    db.session.flush()

    return stock


def update_stock_price(stock):
    price = get_stock_price(stock.symbol)
    
    stock.current_price = price
    
    # db.session.add(stock) is removed here as SQLAlchemy 
    # automatically tracks modifications to attached objects.

    return stock
