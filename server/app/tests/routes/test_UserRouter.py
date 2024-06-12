import pytest
import unittest

from server.app.database.connection import database
from ..conftest import _app
from ..Mock import createSession, DEFAULT_PASSWORD


class TestUserRouter(unittest.TestCase):
    url_prefix = "/user"
    token = ""
    client = pytest.client
    created_users: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()

    @pytest.mark.run(order=11)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no users"
        }
        response = self.client.get(f"{self.url_prefix}/list")
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    # todo: test weak password
    @pytest.mark.run(order=12)
    def test_create_new_user(self):
        for i in range(3):
            expected_response_data = {
                "name": f'user_{i}',
                "email": f'user_{i}@email.com'
            }

            name = f'user_{i}'
            email = f'{name}@email.com'
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": name,
                    "email": email,
                    "password": DEFAULT_PASSWORD
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], str)
            # *** shoud never return the password
            hasPassword = "password" in response.json
            assert hasPassword == False
            assert expected_response_data["name"] == response.json["name"]
            assert expected_response_data["email"] == response.json["email"]
            self.created_users.append(response.json)

    @pytest.mark.run(order=13)
    def test_list_users(self):
        response = self.client.get(f"{self.url_prefix}/list")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_users

    @pytest.mark.run(order=14)
    def test_invalid_token_user(self):
        for user in self.created_users:
            response = self.client.put(
                f"{self.url_prefix}/update",
                json={
                    "name": f"updated_{user['name']}"
                },
                headers={
                    "Authorization": "!NV4L1dT0k3N"
                }
            )
            assert response.status_code == 401


    @pytest.mark.run(order=15)
    def test_update_user(self):
        for user in self.created_users:
            token = createSession(email=user["email"])
            response = self.client.put(
                f"{self.url_prefix}/update",
                json={
                    "name": f"updated_{user['name']}"
                },
                headers={
                    "Authorization": token
                }
            )
            assert response.status_code == 200
            assert response.json["name"] == f"updated_{user['name']}"

    @pytest.mark.run(order=16)
    def test_delete_user(self):
        for user in self.created_users:
            token = createSession(email=user["email"])
            response = self.client.delete(
                f"{self.url_prefix}/delete",
                headers={
                    "Authorization": token
                }
            )
            assert response.status_code == 200
            assert response.json["email"] == user["email"]

    @pytest.mark.run(order=17)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
