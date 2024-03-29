import pytest
import unittest
from server.app.database.connection import database
from ..conftest import _app


class TestUserRouter(unittest.TestCase):
    url_prefix = "/user"
    client = pytest.client
    created_users: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.create_all()
            database.session.commit()

    @pytest.mark.run(order=11)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no users"
        }
        response = self.client.get(f"{self.url_prefix}/list")
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    # todo: test weak password and repeated email
    @pytest.mark.run(order=12)
    def test_create_new_user(self):
        for i in range(3):
            expected_response_data = {
                "name": f'User-{i}',
                "email": f'user_{i}@email.com'
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": f'User-{i}',
                    "email": f'user_{i}@email.com',
                    "password": "password123"
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], str)
            # shoud never return the password
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
    def test_delete_user(self):
        for user in self.created_users:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{user['id']}"
            )
            response.status == 200
            assert response.json == user

    @pytest.mark.run(order=15)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
