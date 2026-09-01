from datetime import datetime

from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL")
    )

    action = db.Column(
        db.String(50),
        nullable=False
    )

    entity_type = db.Column(
        db.String(50)
    )

    entity_id = db.Column(
        db.Integer
    )

    details = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="audit_logs"
    )