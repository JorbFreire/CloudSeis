import pytest
import unittest
from server.app.database.connection import database
from ..conftest import _app
from ..Mock import Mock


class TestLineRouter(unittest.TestCase):
    url_prefix = "/line"
    client = pytest.client
    mock = Mock()
    created_lines: list[dict] = []

    #! this fixture implementation shall be checked to be
    #! fully adopted on ent-to-end tests at this app
    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProject()
            self.mock.loadWorkflow()

        expected_response_data = {
            "Error": "There are no Lines for this project"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}",
            headers={
                "Authorization": self.mock.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=22)
    def test_create_new_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW LINE-{i}',
                "projectId": self.mock.project['id']
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.project['id']}",
                json={
                    "name": f'NEW LINE-{i}',
                    "projectId": self.mock.project['id']
                },
                headers={
                    "Authorization": self.mock.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert expected_response_data["name"] == response.json["name"]
            assert expected_response_data["projectId"] == response.json["projectId"]
            self.created_lines.append(response.json)

    @pytest.mark.run(order=24)
    def test_list_lines(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}",
            headers={
                "Authorization": self.mock.token
            }
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_lines

    @pytest.mark.run(order=25)
    def test_delete_line(self):
        for line in self.created_lines:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{line['id']}",
                headers={
                    "Authorization": self.mock.token
                }
            )
            assert response.status_code == 200

    @pytest.mark.run(order=26)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
