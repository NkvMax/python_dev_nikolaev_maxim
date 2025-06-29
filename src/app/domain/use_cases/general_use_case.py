"""
Агрегируем логи пользователя по дням в формат:
[
    {"date": "2025-01-01", "logins": 1,
     "logouts": 1, "blog_actions": 0},
    ...
]
"""

from collections import defaultdict
from typing import Dict, List

# эти функции патчатся в unit-тестах, поэтому импортируем прямо здесь
from app.services.db.db1_repository import get_user_id_by_login
from app.services.db.db2_repository import get_general_logs_for_user


def _empty_row() -> Dict[str, int]:
    return {"logins": 0, "logouts": 0, "blog_actions": 0}


def get_general_for_user(login: str) -> List[Dict]:
    user_id = get_user_id_by_login(login)
    if user_id is None:
        return []

    raw_rows = get_general_logs_for_user(user_id)

    acc: Dict[str, Dict[str, int]] = defaultdict(_empty_row)

    for row in raw_rows:
        bucket = acc[row["dt"]]

        if row["event_name"] == "login":
            bucket["logins"] += row["total"]
        elif row["event_name"] == "logout":
            bucket["logouts"] += row["total"]
        elif (
            row["event_name"] == "comment"
            and row["space_name"] == "blog"  # блог-действия считаем только в space 'blog'
        ):
            bucket["blog_actions"] += row["total"]

    # сортируем ключи (даты) для стабильного порядка
    return [{"date": dt, **vals} for dt, vals in sorted(acc.items())]


__all__ = ["get_general_for_user"]
