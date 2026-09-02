from app.extensions import db
from app.models.audit_log import AuditLog


def create_audit_log(
    user_id,
    action,
    entity_type=None,
    entity_id=None,
    details=None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )

    db.session.add(audit_log)