from datetime import datetime

from app.extensions import db


class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    cash_balance = db.Column(
        db.Numeric(15, 2),
        nullable=False,
        default=0.00
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

    user = db.relationship(
        "User",
        back_populates="portfolio"
    )

    holdings = db.relationship(
        "Holding",
        back_populates="portfolio",
        cascade="all, delete-orphan"
    )