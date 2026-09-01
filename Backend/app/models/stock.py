from datetime import datetime

from app.extensions import db


class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    company_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Numeric(12, 2), nullable=False)

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

    holdings = db.relationship(
        "Holding",
        back_populates="stock"
    )

    orders = db.relationship(
        "Order",
        back_populates="stock"
    )