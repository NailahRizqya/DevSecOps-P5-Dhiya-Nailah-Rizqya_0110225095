import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture()
def client():
    app = create_app(TestConfig)
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    client.post("/register", json={"username": "budi", "password": "rahasia123"})
    token = client.post(
        "/login", json={"username": "budi", "password": "rahasia123"}
    ).get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
