from unittest.mock import patch

import pytest

from app.domain.use_cases.comments_use_case import get_comments_for_user


@pytest.mark.parametrize(
    "login,user_id",
    [("vladimir", 1), ("ghost", None)],
)
@patch("app.domain.use_cases.comments_use_case.get_comments_rows")
@patch("app.domain.use_cases.comments_use_case.get_user_id_by_login", autospec=True)
def test_get_comments_for_user(mock_uid, mock_rows, login, user_id):
    """Pure-unit: логика ветвления внутри use-case."""
    mock_uid.return_value = user_id
    mock_rows.return_value = (
        [{"user_login": login, "post_header": "HDR",
          "post_author_login": "AUTH", "total_comments": 2}]
        if user_id else []
    )

    result = get_comments_for_user(login)

    if user_id is None:
        assert result == []
        mock_rows.assert_not_called()
    else:
        assert result[0]["total_comments"] == 2
        mock_rows.assert_called_once_with(user_id)
