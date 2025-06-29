"""
Ленивый, "само-настраивающийся" слой доступа к БД.
"""
from __future__ import annotations

import contextlib
import os
import sys
from datetime import datetime
from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


# helpers
def _env_url(*vars_: str) -> str | None:
    for v in vars_:
        url = os.getenv(v)
        if url and "@db" not in url:
            return url
    return None


def _mk_engine(url: str) -> Engine:
    if url.startswith("sqlite"):
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )
    return create_engine(url, pool_pre_ping=True, future=True)


# default engines
@lru_cache
def _content_eng() -> Engine:
    url = _env_url("CONTENT_DATABASE_URL", "DATABASE_URL1") or "sqlite:///:memory:"
    eng = _mk_engine(url)
    _bootstrap_sqlite(eng, is_logs=False)
    return eng


@lru_cache
def _logs_eng() -> Engine:
    url = _env_url("LOGS_DATABASE_URL", "DATABASE_URL2") or "sqlite:///:memory:"
    eng = _mk_engine(url)
    _bootstrap_sqlite(eng, is_logs=True)
    return eng


# session factories
def _ctx_factory(eng_fn):
    @contextlib.contextmanager
    def _ctx() -> Iterator[Session]:
        Ses = sessionmaker(bind=eng_fn(), autoflush=False, expire_on_commit=False)
        session = Ses()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return _ctx


SessionContent = _ctx_factory(_content_eng)  # noqa: N816
SessionLogs = _ctx_factory(_logs_eng)  # noqa: N816


# SQLite seed data
def _bootstrap_sqlite(engine: Engine, *, is_logs: bool) -> None:
    if engine.dialect.name != "sqlite" or getattr(engine, "_seeded", False):
        return

    from app.db.models import Base, Author, Blog, Post, EventType, SpaceType, Log

    Base.metadata.create_all(engine)
    with Session(engine) as s:
        # авторы + один пост
        if not s.scalar(select(func.count(Author.id))):
            a1 = Author(id=1, login="vladimir", email="v@example.com")
            a2 = Author(id=2, login="yanina", email="y@example.com")
            s.add_all([a1, a2,
                       Blog(id=1, name="Demo", author_id=1),
                       Post(id=1, header="HDR", text="TXT", author_id=1, blog_id=1)])

        # словари + три лога
        if is_logs and not s.scalar(select(func.count(EventType.id))):
            et_login, et_logout, et_comment = (EventType(id=i, name=n)
                                               for i, n in [(1, "login"), (2, "logout"), (3, "comment")])
            st_global, st_blog, st_post = (SpaceType(id=i, name=n)
                                           for i, n in [(1, "global"), (2, "blog"), (3, "post")])
            s.add_all([et_login, et_logout, et_comment, st_global, st_blog, st_post,
                       Log(id=1, datetime=datetime(2025, 1, 1), user_id=1,
                           space_type_id=1, event_type_id=1, object_id=0)])

        s.commit()
    engine._seeded = True


# alias для старых импортов app.db.session
sys.modules.setdefault("app.db.session", sys.modules[__name__])

__all__ = ["SessionContent", "SessionLogs"]
