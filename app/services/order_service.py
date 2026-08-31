from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models.order import Order
from app.models.stock import Stock
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.services.audit_service import create_audit_log
from app.services.stock_service import get_stock_price


def create_order(
    user,
    symbol,
    order_type,
    quantity,
    source_ip=None
):
    symbol = symbol.upper()
    order_type = order_type.upper()

    if order_type not in ("BUY", "SELL"):
        raise ValueError("Order type must be BUY or SELL")

    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    portfolio = Portfolio.query.filter_by(
        user_id=user.id
    ).first()

    if not portfolio:
        raise ValueError("Portfolio not found")

    stock = Stock.query.filter_by(
        symbol=symbol
    ).first()

    if not stock:
        price = get_stock_price(symbol)

        stock = Stock(
            symbol=symbol,
            company_name=symbol,
            current_price=price
        )

        db.session.add(stock)
        db.session.flush()

    else:
        price = get_stock_price(symbol)
        stock.current_price = price

    price_decimal = Decimal(str(price))

    if order_type == "BUY":
        total_cost = price_decimal * quantity

        if portfolio.cash_balance < total_cost:
            raise ValueError("Insufficient cash balance")

    elif order_type == "SELL":
        holding = Holding.query.filter_by(
            portfolio_id=portfolio.id,
            stock_id=stock.id
        ).first()

        if not holding or holding.quantity < quantity:
            raise ValueError("Insufficient shares")

    order = Order(
        user_id=user.id,
        stock_id=stock.id,
        order_type=order_type,
        quantity=quantity,
        price=price_decimal,
        status="PENDING",
        created_by=user.id,
        created_from=source_ip
    )

    db.session.add(order)
    db.session.flush()

    create_audit_log(
        user_id=user.id,
        action="CREATE_ORDER",
        entity_type="ORDER",
        entity_id=order.id,
        details=(
            f"Created {order_type} order for "
            f"{quantity} {symbol} shares"
        )
    )

    db.session.commit()

    return order


def get_user_orders(user_id):
    return (
        Order.query
        .filter_by(user_id=user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order(order_id, user_id=None):
    query = Order.query.filter_by(id=order_id)

    if user_id is not None:
        query = query.filter_by(user_id=user_id)

    return query.first()


def cancel_order(order, user, source_ip=None):
    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be cancelled"
        )

    order.status = "CANCELLED"
    order.cancelled_at = datetime.utcnow()
    order.updated_by = user.id
    order.updated_from = source_ip
    order.updated_at = datetime.utcnow()

    create_audit_log(
        user_id=user.id,
        action="CANCEL_ORDER",
        entity_type="ORDER",
        entity_id=order.id,
        details=f"Cancelled order #{order.id}"
    )

    db.session.commit()

    return order


def approve_order(order, admin, source_ip=None):
    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be approved"
        )

    portfolio = Portfolio.query.filter_by(
        user_id=order.user_id
    ).first()

    if not portfolio:
        raise ValueError("Portfolio not found")

    if order.order_type == "BUY":

        total_cost = (
            Decimal(str(order.price))
            * order.quantity
        )

        if portfolio.cash_balance < total_cost:
            raise ValueError("Insufficient cash balance")

        portfolio.cash_balance -= total_cost

        holding = Holding.query.filter_by(
            portfolio_id=portfolio.id,
            stock_id=order.stock_id
        ).first()

        if holding:
            old_quantity = holding.quantity
            old_average = Decimal(
                str(holding.average_price)
            )

            new_quantity = (
                old_quantity + order.quantity
            )

            new_average = (
                (old_average * old_quantity)
                + (
                    Decimal(str(order.price))
                    * order.quantity
                )
            ) / new_quantity

            holding.quantity = new_quantity
            holding.average_price = new_average

        else:
            holding = Holding(
                portfolio_id=portfolio.id,
                stock_id=order.stock_id,
                quantity=order.quantity,
                average_price=order.price,
                created_by=admin.id
            )

            db.session.add(holding)

    elif order.order_type == "SELL":

        holding = Holding.query.filter_by(
            portfolio_id=portfolio.id,
            stock_id=order.stock_id
        ).first()

        if not holding or holding.quantity < order.quantity:
            raise ValueError("Insufficient shares")

        total_value = (
            Decimal(str(order.price))
            * order.quantity
        )

        holding.quantity -= order.quantity
        portfolio.cash_balance += total_value

        if holding.quantity == 0:
            db.session.delete(holding)

    else:
        raise ValueError("Invalid order type")

    order.status = "APPROVED"
    order.approved_by = admin.id
    order.approved_at = datetime.utcnow()
    order.updated_by = admin.id
    order.updated_from = source_ip
    order.updated_at = datetime.utcnow()

    create_audit_log(
        user_id=admin.id,
        action="APPROVE_ORDER",
        entity_type="ORDER",
        entity_id=order.id,
        details=f"Approved order #{order.id}"
    )

    db.session.commit()

    return order


def reject_order(order, admin, source_ip=None):
    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be rejected"
        )

    order.status = "REJECTED"
    order.updated_by = admin.id
    order.updated_from = source_ip
    order.updated_at = datetime.utcnow()

    create_audit_log(
        user_id=admin.id,
        action="REJECT_ORDER",
        entity_type="ORDER",
        entity_id=order.id,
        details=f"Rejected order #{order.id}"
    )

    db.session.commit()

    return order


def flag_order(order, admin, source_ip=None):
    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be flagged"
        )

    order.status = "FLAGGED"
    order.updated_by = admin.id
    order.updated_from = source_ip
    order.updated_at = datetime.utcnow()

    create_audit_log(
        user_id=admin.id,
        action="FLAG_ORDER",
        entity_type="ORDER",
        entity_id=order.id,
        details=f"Flagged order #{order.id} for review"
    )

    db.session.commit()

    return order