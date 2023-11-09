import pytest
import unittest
import json


class TestProjectRouter(unittest.TestCase):
    url_prefix = "/project"
    client = pytest.client
    user_id = "74b72923-597f-4de7-b087-fdb75d7ab1b1"
    created_projects: list[dict] = []

    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no Projects for this user"
        }
        response = self.client.get(f"{self.url_prefix}/list/{self.user_id}")
        assert response.status_code == 404
        assert response.json["error"] == expected_response_data["error"]

    # ! it should run 5 time, but aparently not doing it
    @pytest.mark.parametrize('execution_number', range(5))
    def test_create_new_project(self):
        expected_response_data = {
            "name": "NEW PROJECT",
            "userId": self.user_id
        }
        response = self.client.post(
            f"{self.url_prefix}/create",
            json={
                "name": "NEW PROJECT",
                "userId": self.user_id
            }
        )
        assert response.status_code == 200
        assert isinstance(response.json["id"], int)
        assert expected_response_data["name"] == response.json["name"]
        assert expected_response_data["userId"] == response.json["userId"]
        self.created_projects.append(response.json)

    def test_update_project_name(self):
        new_name = "name changed"
        response = self.client.post(
            # ! [2] is out of range, but should not. Problem on "test_create_new_project"
            f"{self.url_prefix}/update/{self.created_projects[2]['id']}",
            json={
                "name": new_name,
            }
        )
        assert response.status_code == 200
        assert response.json == self.created_projects[2]

    def test_list_projects(self):
        response = self.client.get(f"{self.url_prefix}/list/{self.user_id}")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_projects

    def test_delete_project(self):
        for project in self.created_projects:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{project['id']}"
            )
            response.status == 200
            assert response.json == project
