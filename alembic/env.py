import os, sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app.db.models import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# собираем список URL-ов
urls = [
    os.getenv("DATABASE_URL1"),  # blog_db
    os.getenv("DATABASE_URL2"),  # logs_db
]

# убираем None и дубликаты
urls = [u for i, u in enumerate(urls) if u and u not in urls[:i]]

target_metadata = Base.metadata


def _run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    # офлайн-режим (alembic revision --autogenerate) – достаточно первой БД
    url = urls[0]
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    for url in urls:
        connectable = create_engine(url, poolclass=pool.NullPool)
        with connectable.connect() as connection:
            _run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
