import pytest
import unittest

from server.app.database.connection import database
from ..conftest import _app
from ..utils import get_test_line_data, get_test_user_session


class TestWorkflowRouter(unittest.TestCase):
    url_prefix = "/workflow"
    client = pytest.client
    line_data, project_data, user_data = get_test_line_data()
    lineId = line_data["id"]
    projectId = project_data["id"]
    token = get_test_user_session(user_data["name"])
    created_workflows: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.create_all()

    @pytest.mark.run(order=1)
    def test_empty_get(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/show/1",
            json = {
                "DummyMedia": None
            }, 
            headers = {
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=2)
    def test_create_new_workflow_with_bad_parent(self):
        expected_response_data = {
            'Error': {
                'parentType': ['Must be one of: projectId, lineId.']
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.lineId}",
            json= {
                "name": f'NEW BAD WORKFLOW',
                "parentType": "badParent"
            }, 
            headers = {
                "Authorization": self.token
            }
        )
        assert response.status_code == 422
        assert response.json["Error"] == expected_response_data["Error"]

    def test_create_new_workflow_with_inexistent_project(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.projectId + 99}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "projectId"
            }, 
            headers = {
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    # todo: test bad request cases with dateset to block manual dataset
    def test_create_new_workflow_with_inexistent_line(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.lineId + 99}",
            json = {
                "name": f'NEW BAD WORKFLOW',
                "parentType": "lineId"
            }, 
            headers = {
                "Authorization": self.token
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=2)
    def test_create_new_workflow_at_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parent": {
                    "parentType": "lineId",
                    "parentId": self.lineId
                },
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.lineId}",
                json = {
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "lineId"
                }, 
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            assert response.json["file_name"] == ""
            self.created_workflows.append(response.json)

    @pytest.mark.run(order=2)
    def test_create_new_workflow_at_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parent": {
                    "parentType": "projectId",
                    "parentId": self.projectId
                },
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.projectId}",
                json = {
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "projectId",
                }, 
                headers = {
                    "Authorization": self.token
                }
            )
            print(self.project_data)
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            assert response.json["file_name"] == ""
            self.created_workflows.append(response.json)

    @pytest.mark.run(order=5)
    def test_delete_project(self):
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
                json = {
                    "DummyMedia": None
                }, 
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert response.json == workflow

    @pytest.mark.run(order=6)
    def test_clean_up_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
