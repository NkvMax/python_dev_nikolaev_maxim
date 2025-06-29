"""
Запросы в БД логов.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from sqlalchemy import Date, cast, func, select
from sqlalchemy.orm import Session

from app.db.models import EventType, Log, SpaceType
from app.db.session import SessionLogs


# комментарии пользователя
def get_comment_stats(user_id: int) -> List[Dict[str, Any]]:
    """
    [{"post_id": 1, "total_comments": 3}, ...]
    """
    with SessionLogs() as session:
        ev_comment_id = session.scalar(
            select(EventType.id).where(EventType.name == "comment")
        )

        rows = (
            session.execute(
                select(
                    Log.object_id.label("post_id"),
                    func.count(Log.id).label("total_comments"),
                )
                .where(Log.user_id == user_id,
                       Log.event_type_id == ev_comment_id)
                .group_by(Log.object_id)
            )
            .mappings()
            .all()
        )
        return [dict(r) for r in rows]


# совместимость со старыми тестами/импортами
get_comments_rows = get_comment_stats


# общая статистика по дням
def _date_expr(session: Session):
    """sqlite -> func.date();  Postgres -> CAST(... AS DATE)"""
    if session.bind.dialect.name == "sqlite":
        return func.date(Log.datetime)
    return cast(Log.datetime, Date)


def get_general_logs_for_user(user_id: int) -> List[Dict[str, Any]]:
    """
    [{'dt', 'event_name', 'space_name', 'total'}, ...]
    """
    with SessionLogs() as session:
        date_col = _date_expr(session).label("dt")

        stmt = (
            select(
                date_col,
                EventType.name.label("event_name"),
                SpaceType.name.label("space_name"),
                func.count(Log.id).label("total"),
            )
            .join(EventType, Log.event_type_id == EventType.id)
            .join(SpaceType, Log.space_type_id == SpaceType.id)
            .where(Log.user_id == user_id)
            .group_by(date_col, EventType.name, SpaceType.name)
            .order_by(date_col)
        )

        return [dict(r) for r in session.execute(stmt).mappings().all()]
