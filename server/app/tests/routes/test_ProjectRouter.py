import pytest
import unittest
from server.app.create_app import create_app


def _app():
    app = create_app("test")

    return app


def _client():
    return _app().test_client()


def _runner(self):
    return self._app().test_cli_runner()


class TestProjectRouter(unittest.TestCase):
    url_prefix = "/project"
    client = _client()
    user_id = "74b72923-597f-4de7-b087-fdb75d7ab1b1"

    def test_empty_get(self):
        expected_response = {}
        response = self.client.get(
            f"{self.url_prefix}/list/{self.user_id}")
        assert expected_response in response.data

    def test_new_project(self):
        expected_response = {
            "id": 1,
            "name": "NEW PROJECT",
            "userId": self.user_id
        }
        response = self.client.post(
            f"{self.url_prefix}/create",
            data={
                "name": "NEW PROJECT",
                "userId": "74b72923-597f-4de7-b087-fdb75d7ab1b1"
            }
        )
        assert expected_response in response.data
