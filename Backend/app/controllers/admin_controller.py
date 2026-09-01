from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.middleware.auth import roles_required
from app.models.user import User
from app.models.order import Order
from app.services.order_service import (
    get_order,
    approve_order,
    reject_order,
    flag_order
)
from app.controllers.order_controller import order_to_dict


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


@admin_bp.get("/orders")
@roles_required("ADMIN")
def list_all_orders():
    orders = (
        Order.query
        .order_by(Order.created_at.desc())
        .all()
    )

    return {
        "orders": [
            order_to_dict(order)
            for order in orders
        ]
    }, 200


@admin_bp.post("/orders/<int:order_id>/approve")
@roles_required("ADMIN")
def approve(order_id):
    admin_id = int(get_jwt_identity())

    admin = User.query.get(admin_id)

    if not admin:
        return {
            "error": "Admin user not found"
        }, 404

    order = get_order(order_id)

    if not order:
        return {
            "error": "Order not found"
        }, 404

    try:
        order = approve_order(
            order=order,
            admin=admin,
            source_ip=request.remote_addr
        )

        return {
            "message": "Order approved",
            "order": order_to_dict(order)
        }, 200

    except ValueError as error:
        return {
            "error": str(error)
        }, 400


@admin_bp.post("/orders/<int:order_id>/reject")
@roles_required("ADMIN")
def reject(order_id):
    admin_id = int(get_jwt_identity())

    admin = User.query.get(admin_id)

    if not admin:
        return {
            "error": "Admin user not found"
        }, 404

    order = get_order(order_id)

    if not order:
        return {
            "error": "Order not found"
        }, 404

    try:
        order = reject_order(
            order=order,
            admin=admin,
            source_ip=request.remote_addr
        )

        return {
            "message": "Order rejected",
            "order": order_to_dict(order)
        }, 200

    except ValueError as error:
        return {
            "error": str(error)
        }, 400


@admin_bp.post("/orders/<int:order_id>/flag")
@roles_required("ADMIN")
def flag(order_id):
    admin_id = int(get_jwt_identity())

    admin = User.query.get(admin_id)

    if not admin:
        return {
            "error": "Admin user not found"
        }, 404

    order = get_order(order_id)

    if not order:
        return {
            "error": "Order not found"
        }, 404

    try:
        order = flag_order(
            order=order,
            admin=admin,
            source_ip=request.remote_addr
        )

        return {
            "message": "Order flagged",
            "order": order_to_dict(order)
        }, 200

    except ValueError as error:
        return {
            "error": str(error)
        }, 400