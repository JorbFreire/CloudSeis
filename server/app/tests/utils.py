import pytest
from server.app.database.connection import database
from server.app.models.ProjectModel import ProjectModel
from .conftest import _app
# ! any of this function cant be NEVER used twice with the same args !


def get_test_user_data(name="root"):
    response = pytest.client.post(
        "/user/create",
        json={
            "name": f"user-{name}",
            "email": f"user_{name}@email.com",
            "password": "password123"
        }
    )
    user_data = response.json
    return user_data


def get_test_project_data(name="project"):
    user_data = get_test_user_data(name=name)
    response = pytest.client.post(
        "/project/create",
        json={
            "name": "project-test",
            "userId": user_data["id"],
        }
    )
    project_data = response.json
    return project_data, user_data


def get_test_line_id(name="line") -> [int, int]:
    projectId = get_test_project_data(name=name)["id"]
    response = pytest.client.post(
        "/line/create",
        json={
            "name": "line-test",
            "projectId": projectId,
        }
    )
    lineId = response.json["id"]
    return [projectId, lineId]
