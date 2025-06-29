from __future__ import annotations

"""
Работа с content-БД (authors / blogs / posts).
"""

from typing import Dict, List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Author, Post
from app.db.session import SessionContent


# authors
def get_user_by_login(login: str) -> Optional[Author]:
    """
    Вернуть SQLAlchemy-объект Author или None.
    """
    with SessionContent() as session:
        return session.scalar(select(Author).where(Author.login == login))


def get_user_id_by_login(login: str) -> Optional[int]:
    """
    Вернуть id автора по логину (None, если такого нет).
    """
    author = get_user_by_login(login)
    return author.id if author else None


# posts
def get_posts_info(post_ids: List[int]) -> Dict[int, Tuple[str, str]]:
    """
    На вход:  [10, 11]
    На выход: {10: ('ЖК Эдельвейс', 'vladimir'), 11: ('ЖК Ромашка', 'yanina')}
    """
    if not post_ids:
        return {}

    with SessionContent() as session:
        rows = (
            session.execute(
                select(
                    Post.id,
                    Post.header,
                    Author.login.label("author_login"),
                )
                .join(Author, Post.author_id == Author.id)
                .where(Post.id.in_(post_ids))
            )
            .mappings()
            .all()
        )

    return {r["id"]: (r["header"], r["author_login"]) for r in rows}
