from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.get("")
@jwt_required()
def get_dashboard():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }, 404

    portfolio = user.portfolio

    if not portfolio:
        return {
            "error": "Portfolio not found"
        }, 404

    holdings = []

    for holding in portfolio.holdings:
        current_value = (
            float(holding.quantity) *
            float(holding.stock.current_price)
        )

        holdings.append({
            "symbol": holding.stock.symbol,
            "company_name": holding.stock.company_name,
            "quantity": holding.quantity,
            "average_price": float(holding.average_price),
            "current_price": float(holding.stock.current_price),
            "current_value": current_value
        })

    return {
        "cash_balance": float(portfolio.cash_balance),
        "holdings": holdings
    }, 200