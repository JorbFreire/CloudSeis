import pytest
import unittest
from server.app.database.connection import database
from ..conftest import _app
from ..utils import get_test_user_data, get_test_user_session


class TestProjectRouter(unittest.TestCase):
    url_prefix = "/project"
    client = pytest.client
    user_data = get_test_user_data()
    token = get_test_user_session(user_data["name"])
    user_id = user_data["id"]
    created_projects: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            with database.session.begin():
                database.create_all()

    @pytest.mark.run(order=1)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no Projects for this user"
        }
        response = self.client.get(
            f"{self.url_prefix}/list",
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=2)
    def test_create_new_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW PROJECT-{i}',
                "userId": self.user_id
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": f'NEW PROJECT-{i}',
                },
                headers={
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert expected_response_data["name"] == response.json["name"]
            assert expected_response_data["userId"] == response.json["userId"]
            self.created_projects.append(response.json)

    @pytest.mark.run(order=3)
    def test_update_project_name(self):
        new_name = "name changed"
        self.created_projects[2]["name"] = new_name
        response = self.client.put(
            f"{self.url_prefix}/update/{self.created_projects[2]['id']}",
            json={
                "name": new_name,
            },
            headers={
                "Authorization": self.token
            }
        )
        self.created_projects[2]["modified_at"] = response.json["modified_at"]
        assert response.status_code == 200
        assert response.json == self.created_projects[2]

    @pytest.mark.run(order=4)
    def test_list_projects(self):
        response = self.client.get(
            f"{self.url_prefix}/list",
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_projects

    @pytest.mark.run(order=5)
    def test_delete_project(self):
        for project in self.created_projects:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{project['id']}",
                headers={
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert response.json == project

    @pytest.mark.run(order=6)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
