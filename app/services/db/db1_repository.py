from app.config import MySQLConnector, MYSQL_DB1_CONFIG


def get_user_id_by_login(login: str) -> int or None:
    """
    Возвращает id пользователя из db1.users по логину.
    Если не найден, вернет None.
    """
    conn = MySQLConnector(MYSQL_DB1_CONFIG)
    try:
        query = """
            SELECT id 
            FROM users
            WHERE login = %s
            LIMIT 1
        """
        result = conn.execute_query(query, (login,))
        if result:
            return result[0]["id"]
        else:
            return None
    finally:
        conn.close()
