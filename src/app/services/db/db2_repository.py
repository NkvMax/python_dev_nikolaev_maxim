from app.config import MySQLConnector, MYSQL_DB2_CONFIG


def get_comments_rows(user_id: int):
    """
    Достаем комментарии пользователя (event_type='comment'),
    JOIN-им post, space_type, event_type, и т.д
    Возвращаем сырые строки, где есть:
    - user_login (u.login)
    - post_header (p.header)
    - post_author_login (u2.login)
    - total_comments (агрегация)
    """
    conn = MySQLConnector(MYSQL_DB2_CONFIG)
    try:
        query = """
        SELECT
            u.login AS user_login,
            p.header AS post_header,
            u2.login AS post_author_login,
            COUNT(*) AS total_comments
        FROM logs l
        JOIN event_type e ON l.event_type_id = e.id
        JOIN space_type s ON l.space_type_id = s.id
        -- Подключаемся к db1 "через прямое указание схемы db1"
        JOIN db1.post p ON l.object_id = p.id
        JOIN db1.users u2 ON p.author_id = u2.id
        JOIN db1.users u ON l.user_id = u.id
        WHERE e.name = 'comment'
          AND l.user_id = %s
        GROUP BY u.login, p.header, u2.login
        ORDER BY p.header
        """
        result = conn.execute_query(query, (user_id,))
        return result
    finally:
        conn.close()


def get_general_logs_for_user(user_id: int):
    """
    Достаем сырые логи пользователя,
    (date, event_type, space_type, user_login) -- user_login можно JOIN-ить или
    просто user_id.
    Но для агрегации достаточно (datetime, event_type, space_type)
    """
    conn = MySQLConnector(MYSQL_DB2_CONFIG)
    try:
        query = """
        SELECT
            DATE(l.datetime) AS dt,
            e.name AS event_name,
            s.name AS space_name
        FROM logs l
        JOIN event_type e ON l.event_type_id = e.id
        JOIN space_type s ON l.space_type_id = s.id
        WHERE l.user_id = %s
        ORDER BY l.datetime
        """
        result = conn.execute_query(query, (user_id,))
        return result
    finally:
        conn.close()
