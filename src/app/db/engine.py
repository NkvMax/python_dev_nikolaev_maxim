"""
Тонкая прослойка над connection.py:
  при старте приложения / e2e-тестов вызываем init_engines()
  и подменяем фабрики с SQLite-по-умолчанию на Postgres.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import connection as _conn

# публичные имена — чтобы старые импорты не падали
SessionContent = _conn.SessionContent   # noqa: N816
SessionLogs    = _conn.SessionLogs      # noqa: N816


def init_engines(dsn_content: str, dsn_logs: str) -> None:        # noqa: N802
    """Вызывается из FastAPI `main.py` и из фикстуры `migrated_db`."""
    eng_c = create_engine(dsn_content, pool_pre_ping=True, future=True)
    eng_l = create_engine(dsn_logs,    pool_pre_ping=True, future=True)

    ses_c = sessionmaker(bind=eng_c, autoflush=False, expire_on_commit=False)
    ses_l = sessionmaker(bind=eng_l, autoflush=False, expire_on_commit=False)

    # подмена фабрик в обоих модулях
    globals()["SessionContent"] = _conn.SessionContent = lambda: ses_c()   # type: ignore[assignment]
    globals()["SessionLogs"]    = _conn.SessionLogs    = lambda: ses_l()   # type: ignore[assignment]
