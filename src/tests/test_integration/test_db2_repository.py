"""
Репозитории для logs-БД на демо-данных
"""

from app.services.db.db1_repository import get_user_id_by_login
from app.services.db.db2_repository import (
    get_comments_rows,
    get_general_logs_for_user,
)


def test_get_comments_rows():
    uid = get_user_id_by_login("vladimir")
    rows = get_comments_rows(uid)
    assert len(rows) == 1 and rows[0]["total_comments"] == 1


def test_get_general_logs_for_user():
    uid = get_user_id_by_login("vladimir")
    rows = get_general_logs_for_user(uid)

    assert rows  # не пусто
    assert {r["dt"] for r in rows} == {rows[0]["dt"]}  # одна дата
    assert {r["event_name"] for r in rows} == {
        "login",
        "logout",
        "comment",
    }
