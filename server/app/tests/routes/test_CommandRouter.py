import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..Mock import Mock


class TestCommandRouter:
    url_prefix = "/command"
    client = pytest.client
    mock = Mock()
    created_commands: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProject()
            self.mock.loadLine()
            self.mock.loadWorkflow()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/show/1",
            headers={
                "Authorization": self.mock.token
            }
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_command_with_inexistent_workflow(self):
        expected_response_data = {
            # !"Error": "Workflow does not exist"
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.workflow['id'] + 99}",
            json={
                "name": "NO EXISTING PARENT",
                "parameters": "SUDEFAULT",
                "program_id": 1,
            },
            headers={
                "Authorization": self.mock.token,
            }
        )

        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_command(self):
        # ! needs to mock program, shall fix it when testing adm routes
        for i in range(3):
            expected_response_data = {
                "name": f"NEW COMMAND-{i}",
                "workflowId": self.mock.workflow['id'],
                "parameters": "SUDEFAULT",
                "program_id": 1,
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.workflow['id']}",
                json={
                    "name": f"NEW COMMAND-{i}",
                    "parameters": "SUDEFAULT",
                    "program_id": 1,
                },
                headers={
                    "Authorization": self.mock.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            self.created_commands.append(response.json)

    def test_show_command(self):
        for command in self.created_commands:
            response = self.client.get(
                f"{self.url_prefix}/show/{command['id']}",
                headers={
                    "Authorization": self.mock.token,
                }
            )
            assert response.status_code == 200

    # todo: this test as well as its domains need repair
    def test_update_command(self):
        for command in self.created_commands:
            expected_response_data = {
                "parameters": f"SUDEFAULT-updated-{command['id']}",
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{command['id']}",
                json={
                    "parameters": f"SUDEFAULT-updated-{command['id']}",
                },
                headers={
                    "Authorization": self.mock.token
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['parameters'] == expected_response_data['parameters']

    def test_update_order_command(self):
        pass

    def test_invalid_token_command(self):
        for command in self.created_commands:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{command['id']}",
                headers={
                    "Authorization": "!NV4L1DT0K3N"
                }
            )
            assert response.status_code == 401

    def test_delete_command(self):
        for command in self.created_commands:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{command['id']}",
                headers={
                    "Authorization": self.mock.token
                }
            )
            assert response.status_code == 200
