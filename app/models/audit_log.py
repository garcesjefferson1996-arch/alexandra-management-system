from datetime import datetime


class AuditLog:
    def __init__(self, user, action, reason=None):
        self.user = user.username
        self.action = action
        self.reason = reason
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "user": self.user,
            "action": self.action,
            "reason": self.reason,
            "timestamp": self.timestamp
        }
