import pytest
import unittest

from server.app.database.connection import database
from ..conftest import _app
from ..utils import get_test_workflow_data, get_test_user_session

class TestCommandRouter(unittest.TestCase):
    url_prefix = "/command"
    client = pytest.client
    workflow_data, line_data, project_data, user_data = get_test_workflow_data()
    workflowId = workflow_data["id"]
    lineId = line_data["id"]
    projectId = project_data["id"]    
    token = get_test_user_session(user_data["name"])
    created_commands: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_database(self):
        with _app.app_context():
            database.create_all()

    @pytest.mark.run(order=50)
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
        print(response.json)
        assert response.status_code == 401
        assert response.json["Error"] == expected_response_data["Error"]

    @pytest.mark.run(order=51)
    def test_create_new_command(self):
        for i in range(3):
            expected_response_data = {
                "name": f"NEW COMMAND-{i}",
                "workflowId": self.workflowId,
                "parameters": "SUDEFAULT",
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.workflowId}",
                json = {
                    "name": f"NEW COMMAND-{i}",
                    "parameters": "SUDEFAULT",
                },
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            self.created_commands.append(response.json)

    @pytest.mark.run(order=52)
    def test_show_command(self):
        for command in self.created_commands:
            response = self.client.get(
                f"{self.url_prefix}/show/{command['id']}",
                json = {
                    "DummyMedia": None,
                },
                headers = {
                    "Authorization": self.token,
                }
            )
            assert response.status_code == 200
    

    @pytest.mark.run(order=53)
    def test_update_command(self):
        for i in range(3):
            expected_response_data = {
                "name": f"NEW UPDATED COMMAND-{i}",
                "workflowId": self.workflowId,
                "parameters": "SUANYTHING",
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{self.workflowId}",
                json = {
                    "name": f"NEW COMMAND-{i}",
                    "parameters": "SUDEFAULT",
                },
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json["id"], int)
            assert response.json["name"] == expected_response_data["name"]
            self.created_commands.append(response.json)

    @pytest.mark.run(order=54)
    def test_delete_command(self):
        for command in self.created_commands:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{command['id']}",
                json = {
                    "DummyMedia": None
                }, 
                headers = {
                    "Authorization": self.token
                }
            )
            assert response.status_code == 200

    @pytest.mark.run(order=55)
    def test_create_new_command_with_inexistent_workflow(self):
        expected_response_data = {
            # !"Error": "Workflow does not exist" 
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.workflowId + 99}",
            json = {
                "name": "NO EXISTING PARENT",
                "parameters": "SUDEFAULT",
            },
            headers = {
                "Authorization": self.token,
            }
        )

        assert response.status_code == 404
        assert response.json["Error"] == expected_response_data["Error"]
