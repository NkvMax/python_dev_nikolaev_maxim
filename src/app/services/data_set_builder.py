from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List


def _to_date(val) -> date:
    if isinstance(val, date):
        return val
    if isinstance(val, datetime):
        return val.date()
    return datetime.strptime(val, "%Y-%m-%d").date()


# api/comments
def build_comments_dataset(raw_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return raw_rows


# api/general
def build_general_dataset(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    acc: Dict[date, Dict[str, int]] = defaultdict(
        lambda: {"logins": 0, "logouts": 0, "blog_actions": 0}
    )

    for r in rows:
        day = _to_date(r["dt"])
        ev, space, cnt = r["event_name"], r["space_name"], r["total"]

        if ev == "login":
            acc[day]["logins"] += cnt
        elif ev == "logout":
            acc[day]["logouts"] += cnt
        elif space == "blog":  # create / delete post
            acc[day]["blog_actions"] += cnt

    return [
        {"date": d.isoformat(), **stats}
        for d, stats in sorted(acc.items())
    ]
