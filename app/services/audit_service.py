from app.models.audit_log import AuditLog
from app.repositories.audit_repo import save_log


def log_action(user, action, reason=""):
    audit = AuditLog(user.username, action, reason)
    save_log(audit)
