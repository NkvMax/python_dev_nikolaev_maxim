from app.services.db.db1_repository import get_user_id_by_login
from app.services.db.db2_repository import get_comments_rows
from app.services.data_set_builder import build_comments_dataset


def get_comments_for_user(login: str):
    """
    1) Найти ID пользователя в db1 по логину
    2) В db2 взять записи (logs) типа "comment", объединив их с постами
    3) Сформировать итоговую структуру (comments dataset)
    """
    user_id = get_user_id_by_login(login)
    if user_id is None:
        # Пользователь не найден. Вернуть пустой список, или ошибку
        return []

    # Получаем сырые данные из db2
    raw_data = get_comments_rows(user_id)

    # Превращаем в удобную структуру
    dataset = build_comments_dataset(raw_data)

    return dataset
