from app.services.db.db1_repository import get_user_id_by_login
from app.services.db.db2_repository import get_general_logs_for_user
from app.services.data_set_builder import build_general_dataset


def get_general_for_user(login: str):
    """
    1) Найти user_id в db1.users
    2) Получить логи пользователя (db2.logs) - login, logout, blog_actions и т д
    3) Превратить в агрегированный датасет
    """
    user_id = get_user_id_by_login(login)
    if user_id is None:
        return []

    raw_data = get_general_logs_for_user(user_id)
    dataset = build_general_dataset(raw_data)
    return dataset
