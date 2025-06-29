from unittest.mock import patch
import pytest
from app.domain.use_cases.general_use_case import get_general_for_user


@pytest.mark.parametrize("login,user_id",
                         [("vladimir", 1), ("ghost", None)])
@patch("app.domain.use_cases.general_use_case.get_general_logs_for_user")
@patch("app.domain.use_cases.general_use_case.get_user_id_by_login")
def test_get_general_for_user(mock_uid, mock_raw, login, user_id):
    mock_uid.return_value = user_id
    mock_raw.return_value = (
        [
            {"dt": "2025-01-01", "event_name": "login",  "space_name": "global", "total": 1},
            {"dt": "2025-01-01", "event_name": "logout", "space_name": "global", "total": 1},
            {"dt": "2025-01-01", "event_name": "comment","space_name": "post",   "total": 3},
        ] if user_id else []
    )

    result = get_general_for_user(login)

    if user_id is None:
        assert result == []
        mock_raw.assert_not_called()
    else:
        assert result == [
            {"date": "2025-01-01", "logins": 1,
             "logouts": 1, "blog_actions": 0}
        ]
        mock_raw.assert_called_once_with(user_id)
