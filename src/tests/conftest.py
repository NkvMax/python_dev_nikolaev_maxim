"""
Общие фикстуры для integration / e2e / unit-тестов.
Testcontainers поднимает Postgres, Alembic делает миграции,
init_engines() перенастраивает глобальные Session*.
"""

from pathlib import Path
import time, os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from app.db.engine import init_engines

# Один Postgres-контейнер на сессию тестов
@pytest.fixture(scope="session")
def pg_url() -> str:
    with PostgresContainer("postgres:16-alpine") as pg:
        # контейнер отдает URL сразу, БД может еще стартовать
        time.sleep(1)
        yield pg.get_connection_url()

# 2. Миграции + сид-данные + init_engines
@pytest.fixture(scope="session")
def migrated_db(pg_url: str):
    # "перепривязываем" глобальные factory
    from app.db.engine import init_engines
    init_engines(pg_url, pg_url)

    # чтобы alembic/env.py не схватил host=db
    os.environ["DATABASE_URL1"] = pg_url
    os.environ["DATABASE_URL2"] = pg_url
    os.environ["DATABASE_URL"]  = pg_url  # на всякий

    # Alembic upgrade heads
    alembic_ini = Path(__file__).resolve().parents[2] / "alembic.ini"
    cfg = Config(str(alembic_ini))
    cfg.set_main_option("sqlalchemy.url", pg_url)
    command.upgrade(cfg, "heads")

    # сид-скрипт
    from scripts.seed import run as seed_run
    seed_run()

    yield



# Удобные короткие фикстуры
@pytest.fixture
def db_sessions(migrated_db):
    return migrated_db


@pytest.fixture
def db_session(db_sessions):
    sess = db_sessions["content"]()
    try:
        yield sess
    finally:
        sess.rollback()
        sess.close()


@pytest.fixture
def api_client(migrated_db):
    from app.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)
