
from flask import Blueprint, request
import requests
from flask_jwt_extended import jwt_required

from app.services.stock_service import (
    search_stocks,
    get_stock_price,
)


stock_bp = Blueprint(
    "stocks",
    __name__,
    url_prefix="/api/stocks",
)


@stock_bp.get("/search")
@jwt_required()
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return {
            "error": "Search query is required"
        }, 400

    try:
        results = search_stocks(query)

        return {
            "results": results
        }, 200

    except requests.RequestException:
        return {
            "error": "Finnhub request failed"
        }, 502

    except Exception:
        return {
            "error": "Unable to search stocks"
        }, 502


@stock_bp.get("/<symbol>")
@jwt_required()
def get_price(symbol):
    symbol = symbol.upper().strip()

    if not symbol:
        return {
            "error": "Stock symbol is required"
        }, 400

    try:
        price = get_stock_price(symbol)

        return {
            "symbol": symbol,
            "current_price": price,
        }, 200

    except requests.RequestException:
        return {
            "error": "Finnhub request failed"
        }, 502

    except ValueError as error:
        return {
            "error": str(error)
        }, 404

    except Exception:
        return {
            "error": "Unable to retrieve stock price"
        }, 502
