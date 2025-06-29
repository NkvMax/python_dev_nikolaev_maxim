"""
 Заполняет демо‑данными две базы проекта.
    content_db  – авторы, блоги, посты
    logs_db  – справочники + зеркала сущностей + пример логов пользователей
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    Author,
    Blog,
    Post,
    SpaceType,
    EventType,
    Log,
)
from app.db.session import SessionContent, SessionLogs


# helpers

def get_or_create(
        session: Session,
        model,
        defaults: Optional[Dict] = None,
        **kwargs,
):
    """Удобная обертка: вернуть существующую запись или создать новую."""
    instance = session.scalar(select(model).filter_by(**kwargs))
    if instance is not None:
        return instance

    params = {**(defaults or {}), **kwargs}
    instance = model(**params)
    session.add(instance)
    session.flush()  # получаем id
    return instance


# справочники в logs_db

def seed_reference_logs() -> None:
    with SessionLogs() as db:
        # SpaceType
        for name in ("global", "blog", "post"):
            get_or_create(db, SpaceType, name=name)

        # EventType
        for name in ("login", "logout", "comment", "create_post", "delete_post"):
            get_or_create(db, EventType, name=name)

        db.commit()


# контент в content_db

authors_seed = [
    ("vladimir", "vladimir@example.com"),
    ("yanina", "yanina@example.com"),
    ("natalya", "natalya@example.com"),
]

posts_seed = [
    (
        "ЖК Эдельвейс",
        "Описание ЖК Эдельвейс, вид на море, узкий проезд",
    ),
    (
        "ЖК Ромашка",
        "Описание ЖК Ромашка, удобный район, рядом Калина Молл",
    ),
    (
        "ЖК Ландыши",
        "Описание ЖК Ландыши, близость к центру, фитнес‑зал, детплощадки",
    ),
]


def seed_content() -> None:
    with SessionContent() as db:
        authors: list[Author] = [
            get_or_create(db, Author, login=login, email=email) for login, email in authors_seed
        ]

        for author, (header, text) in zip(authors, posts_seed):
            blog = get_or_create(
                db,
                Blog,
                owner_id=author.id,
                name=f"Блог {author.login.capitalize()} о Недвижимости",
                description="Отзывы, мнения, обзоры",
            )
            get_or_create(
                db,
                Post,
                header=header,
                text=text,
                author_id=author.id,
                blog_id=blog.id,
            )
        db.commit()


# копируем Author/Blog/Post из content_db в logs_db

def replicate_content_to_logs() -> None:
    """Чтобы в logs_db корректно работали FK – перенесем сущности‑зеркала"""
    with SessionContent() as cdb, SessionLogs() as ldb:
        # Authors first
        for author in cdb.scalars(select(Author)).all():
            get_or_create(
                ldb,
                Author,
                id=author.id,
                login=author.login,
                email=author.email,
            )

        # Blogs next (FK -> Author)
        for blog in cdb.scalars(select(Blog)).all():
            get_or_create(
                ldb,
                Blog,
                id=blog.id,
                owner_id=blog.owner_id,
                name=blog.name,
                description=blog.description,
            )

        # Posts last (FK -> Blog & Author)
        for post in cdb.scalars(select(Post)).all():
            get_or_create(
                ldb,
                Post,
                id=post.id,
                header=post.header,
                text=post.text,
                author_id=post.author_id,
                blog_id=post.blog_id,
            )
        ldb.commit()


# демо‑логи пользователей

def seed_logs() -> None:
    with SessionContent() as cdb:
        authors = {a.login: a for a in cdb.scalars(select(Author)).all()}
        posts = {p.header: p for p in cdb.scalars(select(Post)).all()}

    with SessionLogs() as ldb:
        # справочники
        st_global: SpaceType = ldb.scalar(select(SpaceType).filter_by(name="global"))
        st_post: SpaceType = ldb.scalar(select(SpaceType).filter_by(name="post"))
        ev_login: EventType = ldb.scalar(select(EventType).filter_by(name="login"))
        ev_comment: EventType = ldb.scalar(select(EventType).filter_by(name="comment"))
        ev_logout: EventType = ldb.scalar(select(EventType).filter_by(name="logout"))

        if ldb.scalar(select(Log.id).limit(1)):
            return  # уже сидированы

        now = datetime.now(timezone.utc)

        def make_logs(user_login: str, post_header: str):
            uid = authors[user_login].id
            pid = posts[post_header].id
            return [
                Log(datetime=now, user_id=uid, space_type_id=st_global.id, event_type_id=ev_login.id, object_id=0),
                Log(datetime=now, user_id=uid, space_type_id=st_post.id, event_type_id=ev_comment.id, object_id=pid),
                Log(datetime=now, user_id=uid, space_type_id=st_global.id, event_type_id=ev_logout.id, object_id=0),
            ]

        ldb.add_all(make_logs("vladimir", "ЖК Эдельвейс"))
        ldb.add_all(make_logs("yanina", "ЖК Ромашка"))
        ldb.add_all(make_logs("natalya", "ЖК Ландыши"))
        ldb.commit()


# entry point

def run() -> None:
    seed_reference_logs()
    seed_content()
    replicate_content_to_logs()
    seed_logs()
    print(">>> demo data inserted")


if __name__ == "__main__":
    run()
