import pytest
import unittest
import json


class TestProjectRouter(unittest.TestCase):
    url_prefix = "/project"
    client = pytest.client
    user_id = "74b72923-597f-4de7-b087-fdb75d7ab1b1"

    def test_empty_get(self):
        expected_response = {}
        response = self.client.get(
            f"{self.url_prefix}/list/{self.user_id}")
        assert expected_response in response.data

    def test_new_project(self):
        expected_response = {
            "name": "NEW PROJECT",
            "userId": self.user_id
        }
        response = self.client.post(
            f"{self.url_prefix}/create",
            json={
                "name": "NEW PROJECT",
                "userId": "74b72923-597f-4de7-b087-fdb75d7ab1b1"
            }
        )
        reponse_dict = json.loads(response.data.decode())
        assert isinstance(reponse_dict["id"], int)
        assert expected_response["name"] == reponse_dict["name"]
        assert expected_response["userId"] == reponse_dict["userId"]
