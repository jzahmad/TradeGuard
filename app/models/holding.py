from datetime import datetime

from app.extensions import db


class Holding(db.Model):
    __tablename__ = "holdings"

    id = db.Column(db.Integer, primary_key=True)

    portfolio_id = db.Column(
        db.Integer,
        db.ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False
    )

    stock_id = db.Column(
        db.Integer,
        db.ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    average_price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

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
        back_populates="holdings"
    )

    stock = db.relationship(
        "Stock",
        back_populates="holdings"
    )