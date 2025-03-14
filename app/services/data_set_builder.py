from collections import defaultdict


def build_comments_dataset(raw_rows):
    """
    Ожидаем, что raw_rows - это список словарей, где есть ключи:
      user_login, post_header, post_author_login, total_comments
    Вернем их как есть (или можно дополнительно обработать).
    """
    results = []
    for row in raw_rows:
        results.append({
            "user_login": row["user_login"],
            "post_header": row["post_header"],
            "post_author_login": row["post_author_login"],
            "total_comments": row["total_comments"]
        })
    return results


def build_general_dataset(raw_rows):
    """
    raw_rows - список словарей, где есть:
      dt (дата), event_name, space_name
    Нужно сгруппировать по dt:
      - кол-во logins (event_name='login')
      - кол-во logouts (event_name='logout')
      - кол-во blog_actions (space_name='blog')
    """
    agg = defaultdict(lambda: {"logins": 0, "logouts": 0, "blog_actions": 0})

    for row in raw_rows:
        date_val = row["dt"]
        event_name = row["event_name"]
        space_name = row["space_name"]

        if event_name == "login":
            agg[date_val]["logins"] += 1
        elif event_name == "logout":
            agg[date_val]["logouts"] += 1

        # Подсчитаем все действия в пространстве "blog"
        if space_name == "blog":
            agg[date_val]["blog_actions"] += 1

    # Превращаем agg в список
    results = []
    for dt, counters in agg.items():
        results.append({
            "date": dt,
            "logins": counters["logins"],
            "logouts": counters["logouts"],
            "blog_actions": counters["blog_actions"]
        })

    # Сортируем по дате (опционально)
    results.sort(key=lambda x: x["date"])
    return results
