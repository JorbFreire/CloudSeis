import pytest
from dotenv import load_dotenv

from server.app.create_app import create_app

load_dotenv()
_app = create_app("test")


def _client():
    return _app.test_client()


def _runner():
    return _app.test_cli_runner()


def pytest_configure():
    pytest.client = _client()
