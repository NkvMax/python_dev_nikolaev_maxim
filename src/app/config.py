import os
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor

# Загрузка переменных окружения
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Конфиг для db1
MYSQL_DB1_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DB1_NAME", "db1"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

# Конфиг для db2
MYSQL_DB2_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DB2_NAME", "db2"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}


class MySQLConnector:
    """
    Универсальный класс для подключения к MySQL.
    При инициализации передаем конфиг словарем
    """
    def __init__(self, config: dict):
        self.connection = pymysql.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            port=config["port"],
            cursorclass=DictCursor
        )

    def execute_query(self, query: str, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.fetchall()

    def close(self):
        self.connection.close()
