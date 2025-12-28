import json
import os
from app.models.audit_log import AuditLog

DATA_FILE = "app/data/audit_logs.json"


def load_logs():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_log(log: AuditLog):
    logs = load_logs()
    logs.append(log.to_dict())

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
