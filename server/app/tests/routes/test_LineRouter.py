import pytest
import unittest
from server.app.database.connection import database
from server.app.models.UserModel import UserModel
from server.app.models.ProjectModel import ProjectModel
from ..conftest import _app
from ..utils import get_test_project_data, get_test_user_session


class TestLineRouter(unittest.TestCase):
    url_prefix = "/line"
    client = pytest.client
    project_data, user_data = get_test_project_data()
    token = get_test_user_session(user_data["name"])
    project_id = project_data["id"]
    created_lines: list[dict] = []

    #! this fixture implementation shall be checked to be
    #! fully adopted on ent-to-end tests at this app
    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            with database.session.begin():
                database.create_all()
                user = UserModel(**self.user_data)
                project = ProjectModel(**self.project_data)
                database.session.add(user)
                database.session.add(project)
                database.session.commit()

        expected_response_data = {
            "Error": "There are no Lines for this project"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/{self.project_id}",
            json = {
                "DummyMedia": None
            }, 
            headers = {
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=22)
    def test_create_new_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW LINE-{i}',
                "projectId": self.project_id
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.project_id}",
                json={
                    "name": f'NEW LINE-{i}',
                }, 
                headers = {
                    "Authorization": self.token
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
            f"{self.url_prefix}/list/{self.project_id}",
            json = {
                "DummyMedia": None
            }, 
            headers = {
                "Authorization": self.token
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
                json = {
                    "DummyMedia": None
                }, 
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200

    @pytest.mark.run(order=26)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
