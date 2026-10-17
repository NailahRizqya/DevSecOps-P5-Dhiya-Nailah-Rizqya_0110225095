import pytest

from app import create_app
from app.config import Config


def test_app_requires_secret_key():
    class NoSecret(Config):
        SECRET_KEY = ""
        DATABASE = ":memory:"

    with pytest.raises(RuntimeError):
        create_app(NoSecret)


def test_app_with_file_database(tmp_path):
    class FileDb(Config):
        SECRET_KEY = "k"
        DATABASE = str(tmp_path / "t.db")
        TESTING = True

    client = create_app(FileDb).test_client()
    assert client.get("/health").status_code == 200
