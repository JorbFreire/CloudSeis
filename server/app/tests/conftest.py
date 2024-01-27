import pytest
from server.app.create_app import create_app


_app = create_app("test")


def _client():
    return _app.test_client()


def _runner():
    return _app.test_cli_runner()


def pytest_configure():
    pytest.client = _client()
