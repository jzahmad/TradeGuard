from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    stock_id = db.Column(
        db.Integer,
        db.ForeignKey("stocks.id", ondelete="RESTRICT"),
        nullable=False
    )

    order_type = db.Column(
        db.String(10),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL")
    )

    approved_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)

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

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="orders"
    )

    approver = db.relationship(
        "User",
        foreign_keys=[approved_by],
        back_populates="approved_orders"
    )

    stock = db.relationship(
        "Stock",
        back_populates="orders"
    )