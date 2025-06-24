import pytest
from app.services.db.db1_repository import get_user_id_by_login
from app.config import MYSQL_DB1_CONFIG, MySQLConnector


@pytest.fixture(scope="module")
def setup_db1():
    """
    Фикстура для подготовки тестовой базы db1:
    Вставляем тестового пользователя Sergey если его нет
    """
    conn = MySQLConnector(MYSQL_DB1_CONFIG)
    try:
        # Используем INSERT с ON DUPLICATE KEY UPDATE, чтобы не дублировать, если пользователь уже есть
        query = """
            INSERT INTO users (login, email)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE email = VALUES(email)
        """
        conn.execute_query(query, ("Sergey", "sergey@example.com"))
        yield
    finally:
        conn.close()


def test_get_user_id_by_login_existing(setup_db1):
    """
    Проверяем, что для существующего пользователя функция возвращает корректный user_id
    """
    user_id = get_user_id_by_login("Sergey")
    assert user_id is not None
    assert isinstance(user_id, int)


def test_get_user_id_by_login_nonexistent():
    """
    Если пользователь не найден, функция должна вернуть None
    """
    user_id = get_user_id_by_login("nonexistent_user_xyz")
    assert user_id is None
