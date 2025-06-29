"""
  Проверяем, что session-factory из конфигурации
   правильно работает с demo-данными (scripts/seed.py).
"""

from app.services.db.db1_repository import get_user_id_by_login


def test_get_user_id_by_login_found():
    uid = get_user_id_by_login("vladimir")
    assert isinstance(uid, int) and uid > 0


def test_get_user_id_by_login_not_found():
    assert get_user_id_by_login("nonexistent_login_123") is None
