import pytest
from app.services.db.db2_repository import get_comments_rows, get_general_logs_for_user
from app.config import MYSQL_DB2_CONFIG, MYSQL_DB1_CONFIG, MySQLConnector


@pytest.fixture(scope="module")
def db2_setup():
    """
    Фикстура для подготовки тестовых данных:
    - В db2 очищаем и вставляем справочники (space_type, event_type)
    - В db1 вставляем тестового пользователя Vadim, а также блог/пост Vadim Blog,
      чтобы при вставке логов был реальный post_id.
    - Затем вставляем в db2 несколько логов, используя id созданного поста
    """
    # Очищаем db2
    conn2 = MySQLConnector(MYSQL_DB2_CONFIG)
    conn2.execute_query("DELETE FROM logs")
    conn2.execute_query("DELETE FROM space_type")
    conn2.execute_query("DELETE FROM event_type")

    # Вставляем справочники
    conn2.execute_query("INSERT INTO space_type(name) VALUES ('global'), ('blog'), ('post')")
    conn2.execute_query("INSERT INTO event_type(name) VALUES ('login'), ('logout'), ('comment'), ('create_post')")

    # Подготавливаем db1
    conn1 = MySQLConnector(MYSQL_DB1_CONFIG)
    # Создаем или обновляем пользователя с логином Vadim
    conn1.execute_query(
        "INSERT INTO users (login, email) VALUES (%s, %s) ON DUPLICATE KEY UPDATE email=VALUES(email)",
        ("Vadim", "vadim@example.com")
    )
    # Получаем id пользователя Vadim
    vadim_user = conn1.execute_query("SELECT id FROM users WHERE login = %s LIMIT 1", ("Vadim",))[0]
    vadim_user_id = vadim_user["id"]

    # Создаем или обновляем блог "Vadim Blog"
    conn1.execute_query(
        """
        INSERT INTO blog (owner_id, name, description)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name)
        """,
        (vadim_user_id, "Vadim Blog", "Vadim blog description")
    )
    vadim_blog = conn1.execute_query("SELECT id FROM blog WHERE name = %s LIMIT 1", ("Vadim Blog",))[0]
    vadim_blog_id = vadim_blog["id"]

    # Создаем или обновляем пост "Vadim Post"
    conn1.execute_query(
        "INSERT INTO post (header, text, author_id, blog_id) VALUES (%s, %s, %s, %s)",
        ("Vadim Post", "Some text for Vadim's post", vadim_user_id, vadim_blog_id)
    )
    vadim_post = conn1.execute_query("SELECT id FROM post WHERE header = %s LIMIT 1", ("Vadim Post",))[0]
    vadim_post_id = vadim_post["id"]

    # Теперь вставляем логи в db2, привязывая к user_id=1 и vadim_post_id (просто для теста)
    conn2.execute_query(
        """
        INSERT INTO logs (`datetime`, user_id, space_type_id, event_type_id, object_id)
        VALUES
        ('2023-01-01 10:00:00', 1,
            (SELECT id FROM space_type WHERE name = 'post'),
            (SELECT id FROM event_type WHERE name = 'comment'),
            %s
        ),
        ('2023-01-01 11:00:00', 1,
            (SELECT id FROM space_type WHERE name = 'global'),
            (SELECT id FROM event_type WHERE name = 'login'),
            NULL
        );
        """,
        (vadim_post_id,)
    )

    yield

    # После тестов можно почистить:
    conn2.execute_query("DELETE FROM logs")
    conn2.execute_query("DELETE FROM space_type")
    conn2.execute_query("DELETE FROM event_type")
    conn2.close()
    conn1.close()


def test_get_comments_rows(db2_setup):
    """
    Проверяем, что get_comments_rows(user_id=1) возвращает 1 запись по комментарию
    """
    result = get_comments_rows(user_id=1)
    assert len(result) == 1


def test_get_general_logs_for_user(db2_setup):
    """
    Проверяем, что get_general_logs_for_user(user_id=1) возвращает 2 записи (одна 'comment', одна 'login')
    """
    result = get_general_logs_for_user(user_id=1)
    assert len(result) == 2
