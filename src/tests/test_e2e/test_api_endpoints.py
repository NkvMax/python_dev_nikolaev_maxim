from fastapi.testclient import TestClient


def test_comments_endpoint(api_client: TestClient):
    resp = api_client.get("/api/comments/?login=vladimir")
    data = resp.json()
    assert resp.status_code == 200
    assert data["data"][0]["total_comments"] == 1


def test_general_endpoint(api_client: TestClient):
    resp = api_client.get("/api/general/?login=vladimir")
    data = resp.json()
    assert resp.status_code == 200
    assert data["data"][0]["logins"] == 1
