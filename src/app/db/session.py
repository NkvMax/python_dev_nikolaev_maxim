# Тонкий ре-экспорт: старый импорт
#     from app.db.connection import SessionContent
# продолжает работать.

from app.db.engine import SessionContent, SessionLogs  # noqa: F401
