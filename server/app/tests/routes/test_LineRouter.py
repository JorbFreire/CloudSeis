import pytest
import unittest
from server.app.database.connection import database
from ..conftest import _app
from ..utils import get_test_project_id


class TestProjectRouter(unittest.TestCase):
    url_prefix = "/line"
    client = pytest.client
    project_id = get_test_project_id()
    created_lines: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.create_all()

    @pytest.mark.run(order=1)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no Lines for this project"
        }
        response = self.client.get(f"{self.url_prefix}/list/{self.project_id}")
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=2)
    def test_create_new_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW LINE-{i}',
                "projectId": self.project_id
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": f'NEW LINE-{i}',
                    "projectId": self.project_id
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert expected_response_data["name"] == response.json["name"]
            assert expected_response_data["projectId"] == response.json["projectId"]
            self.created_lines.append(response.json)

    @pytest.mark.run(order=4)
    def test_list_projects(self):
        response = self.client.get(f"{self.url_prefix}/list/{self.project_id}")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_lines

    @pytest.mark.run(order=5)
    def test_delete_project(self):
        for line in self.created_lines:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{line['id']}"
            )
            response.status == 200
            assert response.json == line

    @pytest.mark.run(order=6)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
