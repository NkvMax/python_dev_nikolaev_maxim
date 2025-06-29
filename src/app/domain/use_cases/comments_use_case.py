"""
Возвращает агрегат "топ-посты и количество комментариев" для заданного
пользователя.

Unit-тесты мокируют обе функции (`get_user_id_by_login`,
`get_comments_rows`) — поэтому внутри кейса только развилка.
"""
from typing import Dict, List

from app.services.db.db1_repository import get_user_id_by_login  # alias для @patch
from app.services.db.db2_repository import get_comments_rows     # alias для @patch


def get_comments_for_user(login: str) -> List[Dict]:
    user_id = get_user_id_by_login(login)
    if user_id is None:
        return []

    return get_comments_rows(user_id)
