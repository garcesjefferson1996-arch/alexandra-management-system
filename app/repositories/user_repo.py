import json
import os
from app.models.user import User

DATA_FILE = "app/data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [User(**u) for u in data]
        except json.JSONDecodeError:
            return []


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=4)
