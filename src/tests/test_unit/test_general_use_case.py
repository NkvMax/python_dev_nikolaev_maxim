import pytest
from unittest.mock import patch
from app.domain.use_cases.general_use_case import get_general_for_user


@pytest.mark.parametrize("login,user_id", [
    ("Andrey", 1),
    ("nonexistent", None),
])
@patch("app.domain.use_cases.general_use_case.get_user_id_by_login")
@patch("app.domain.use_cases.general_use_case.get_general_logs_for_user")
def test_get_general_for_user(mock_get_general_logs, mock_get_user_id, login, user_id):
    """
    Тест для проверки общей бизнес-логики
    Если пользователь не найден, функция должна вернуть пустой список
    Если найден, то возвращаем агрегированные данные
    """
    # Настраиваем поведение моков:
    mock_get_user_id.return_value = user_id
    if user_id is not None:
        # Симулируем возвращение двух логов для одного дня
        mock_get_general_logs.return_value = [
            {"dt": "2023-01-01", "event_name": "login",  "space_name": "global"},
            {"dt": "2023-01-01", "event_name": "logout", "space_name": "global"},
        ]
    else:
        mock_get_general_logs.return_value = []

    result = get_general_for_user(login)

    if user_id is None:
        # Если пользователь не найден, то и логов не должно запрашиваться.
        assert result == []
        mock_get_general_logs.assert_not_called()
    else:
        # Проверяем, что функция возвращает агрегированные данные
        # В данном случае агрегируем данные по дате "2023-01-01"
        assert isinstance(result, list)
        # Ожидаем одну агрегированную запись по дате "2023-01-01"
        assert len(result) == 1
        aggregated = result[0]
        assert aggregated["date"] == "2023-01-01"
        # Ожидаем, что для логина и логаута будет по одному
        assert aggregated["logins"] == 1
        assert aggregated["logouts"] == 1
