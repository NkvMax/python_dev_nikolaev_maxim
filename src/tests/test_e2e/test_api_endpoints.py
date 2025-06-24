import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """
    Опционально: здесь можно поднять/очистить тестовую БД,
    """
    yield


def test_comments_endpoint():
    """
    et2-тест для эндпоинта /api/comments?login=john
    """
    response = client.get("/api/comments?login=john")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    # Проверим структуру
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        row = data["data"][0]
        assert "user_login" in row
        assert "post_header" in row
        assert "post_author_login" in row
        assert "total_comments" in row


def test_general_endpoint():
    """
    e2e-тест для эндпоинта /api/general?login=john
    """
    response = client.get("/api/general?login=john")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    # Проверим структуру
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        row = data["data"][0]
        assert "date" in row
        assert "logins" in row
        assert "logouts" in row
        assert "blog_actions" in row
