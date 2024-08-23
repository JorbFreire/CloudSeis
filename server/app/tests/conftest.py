import pytest
from dotenv import load_dotenv

from server.app.create_app import create_app

load_dotenv()
_app = create_app("test")

def _client():
    return _app.test_client()

def pytest_configure():
    pytest.client = _client()

def pytest_collection_modifyitems(items):
    CLASS_ORDER = [ "TestUserRouter", "TestProjectRouter", "TestLineRouter", "TestWorkflowRouter" ]
    sorted_items = items.copy()
    class_mapping = {item: item.cls.__name__ for item in items if hasattr(item, 'cls') and item.cls}

    for class_ in CLASS_ORDER:
        sorted_items = [it for it in sorted_items if class_mapping[it] != class_] + [
            it for it in sorted_items if class_mapping[it] == class_
        ]


    items[:] = sorted_items
