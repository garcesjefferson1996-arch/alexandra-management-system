from app.models.audit_log import AuditLog
from app.repositories.audit_repo import save_log


def log_action(user, action, reason=None):
    log = AuditLog(
        user=user,
        action=action,
        reason=reason
    )
    save_log(log)

