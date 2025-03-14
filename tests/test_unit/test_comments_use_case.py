import pytest
from unittest.mock import patch
from app.domain.use_cases.comments_use_case import get_comments_for_user


@pytest.mark.parametrize("login,user_id", [
    ("Andrey", 1),
    ("Vadim", 2),
    ("unknown_user", None),
])
@patch("app.domain.use_cases.comments_use_case.get_user_id_by_login")
@patch("app.domain.use_cases.comments_use_case.get_comments_rows")
def test_get_comments_for_user(mock_get_comments_rows, mock_get_user_id_by_login, login, user_id):
    """
    Тестируем бизнес-логику get_comments_for_user,
    подменивая доступ к БД (get_user_id_by_login, get_comments_rows).
    """
    # Настраиваем поведение моков
    mock_get_user_id_by_login.return_value = user_id
    mock_get_comments_rows.return_value = [
        {
            "user_login": login,
            "post_header": "Sample Post",
            "post_author_login": "Sergey",
            "total_comments": 3
        }
    ] if user_id else []

    result = get_comments_for_user(login)

    if user_id is None:
        # ожидаем пустой список, так как пользователь не найден
        assert result == []
        mock_get_comments_rows.assert_not_called()
    else:
        # если user_id найден, возвращаем список
        assert len(result) == 1
        assert result[0]["total_comments"] == 3
        mock_get_comments_rows.assert_called_once()
