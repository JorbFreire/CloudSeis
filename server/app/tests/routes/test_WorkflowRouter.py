import pytest
import unittest

from server.app.database.connection import database
from server.app.models.UserModel import UserModel
from server.app.models.ProjectModel import ProjectModel
from server.app.models.LineModel import LineModel
from ..conftest import _app
from ..utils import get_test_line_data, get_test_user_session


class TestWorkflowRouter(unittest.TestCase):
    url_prefix = "/workflow"
    client = pytest.client
    line_data, project_data, user_data = get_test_line_data()
    token = get_test_user_session(user_data["name"])
    created_workflows: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            with database.session.begin():
                database.drop_all()
                database.create_all()
                del self.line_data["workflows"]

                user = UserModel(**self.user_data)
                project = ProjectModel(**self.project_data)
                line = LineModel(**self.line_data, owner_email=user.email)
                database.session.add(user)
                database.session.add(project)
                database.session.add(line)
                database.session.commit()

    @pytest.mark.run(order=31)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/show/1",
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=32)
    def test_create_new_workflow_with_bad_parent(self):
        expected_response_data = {
            'Error': {
                'parentType': ['Must be one of: projectId, lineId.']
            }
        }
        print("self.line_data:")
        print(self.line_data)
        response = self.client.post(
            f"{self.url_prefix}/create/{self.line_data['id']}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "badParent"
            },
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 422
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=33)
    def test_create_new_workflow_with_inexistent_project(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.project_data['id'] + 99}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "projectId"
            },
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    # todo: test bad request cases with dateset to block manual dataset
    @pytest.mark.run(order=34)
    def test_create_new_workflow_with_inexistent_line(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.line_data['id'] + 99}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "lineId"
            },
            headers={
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=35)
    def test_create_new_workflow_at_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parentType": "lineId",
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.line_data['id']}",
                json={
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "lineId"
                },
                headers={
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            assert response.json["file_name"] == ""
            self.created_workflows.append(response.json)

    @pytest.mark.run(order=36)
    def test_create_new_workflow_at_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parent": {
                    "parentType": "projectId",
                    "parentId": self.project_data["id"]
                },
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.project_data['id']}",
                json={
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "projectId",
                },
                headers={
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            assert response.json["file_name"] == ""
            self.created_workflows.append(response.json)

    @pytest.mark.run(order=37)
    def test_delete_project(self):
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
                headers={
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert response.json == workflow

    @pytest.mark.run(order=38)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
