import requests
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User
from app.services.order_service import (
    create_order,
    get_user_orders,
    get_order,
    cancel_order
)


order_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/api/orders"
)


def order_to_dict(order):
    return {
        "id": order.id,
        "symbol": order.stock.symbol,
        "company_name": order.stock.company_name,
        "order_type": order.order_type,
        "quantity": order.quantity,
        "price": float(order.price),
        "status": order.status,
        "created_at": order.created_at.isoformat()
        if order.created_at else None,
        "approved_at": order.approved_at.isoformat()
        if order.approved_at else None,
        "cancelled_at": order.cancelled_at.isoformat()
        if order.cancelled_at else None
    }


@order_bp.post("")
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }, 404

    data = request.get_json() or {}

    symbol = data.get("symbol")
    order_type = data.get("order_type")
    quantity = data.get("quantity")

    if not symbol or not order_type or quantity is None:
        return {
            "error": "symbol, order_type and quantity are required"
        }, 400

    try:
        quantity = int(quantity)

        order = create_order(
            user=user,
            symbol=symbol,
            order_type=order_type,
            quantity=quantity,
            source_ip=request.remote_addr
        )

        return {
            "message": "Order created",
            "order": order_to_dict(order)
        }, 201

    except ValueError as error:
        return {
            "error": str(error)
        }, 400

    except requests.RequestException:
        return {
            "error": "Unable to reach price service, please try again"
        }, 502

    except RuntimeError as error:
        return {
            "error": str(error)
        }, 502


@order_bp.get("")
@jwt_required()
def list_orders():
    user_id = int(get_jwt_identity())

    orders = get_user_orders(user_id)

    return {
        "orders": [
            order_to_dict(order)
            for order in orders
        ]
    }, 200


@order_bp.get("/<int:order_id>")
@jwt_required()
def get_single_order(order_id):
    user_id = int(get_jwt_identity())

    order = get_order(
        order_id=order_id,
        user_id=user_id
    )

    if not order:
        return {
            "error": "Order not found"
        }, 404

    return {
        "order": order_to_dict(order)
    }, 200


@order_bp.delete("/<int:order_id>")
@jwt_required()
def cancel(order_id):
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }, 404

    order = get_order(
        order_id=order_id,
        user_id=user_id
    )

    if not order:
        return {
            "error": "Order not found"
        }, 404

    try:
        order = cancel_order(
            order=order,
            user=user,
            source_ip=request.remote_addr
        )

        return {
            "message": "Order cancelled",
            "order": order_to_dict(order)
        }, 200

    except ValueError as error:
        return {
            "error": str(error)
        }, 400