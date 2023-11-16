import pytest
from server.app.create_app import create_app


_app = create_app("test")


def _client():
    return _app.test_client()


def _runner():
    return _app.test_cli_runner()


def pytest_configure():
    pytest.client = _client()


# this function cant be runned twice before reset the database
def get_root_user_id():
    response = pytest.client.post(
        "/user/create",
        json={
            "name": "user-root",
            "email": "user_root@email.com",
            "password": "password123"
        }
    )
    user_id = response.json["id"]
    return user_id
