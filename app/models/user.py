from datetime import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="USER")

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    created_by = db.Column(db.Integer)
    created_from = db.Column(db.String(255))

    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer)
    updated_from = db.Column(db.String(255))

    portfolio = db.relationship(
        "Portfolio",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        foreign_keys="Order.user_id",
        back_populates="user"
    )

    approved_orders = db.relationship(
        "Order",
        foreign_keys="Order.approved_by",
        back_populates="approver"
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="user"
    )