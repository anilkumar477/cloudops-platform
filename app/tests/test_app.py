from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"CloudOps Platform is running!" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_app_info():
    client = app.test_client()

    response = client.get("/api/info")

    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "CloudOps Platform"
    assert data["version"] == "1.0.0"
    assert data["environment"] == "development"
