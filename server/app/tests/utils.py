import pytest
# any of this function cant be used twice with the same args


def get_test_user_id(name="root") -> str:
    response = pytest.client.post(
        "/user/create",
        json={
            "name": f"user-{name}",
            "email": f"user_{name}@email.com",
            "password": "password123"
        }
    )
    user_id = response.json["id"]
    return user_id


def get_test_project_id(name="project") -> int:
    userId = get_test_user_id(name=name)
    response = pytest.client.post(
        "/project/create",
        json={
            "name": "project-test",
            "userId": userId,
        }
    )
    project_id = response.json["id"]
    return project_id


def get_test_line_id(name="line") -> [int, int]:
    projectId = get_test_project_id(name=name)
    response = pytest.client.post(
        "/line/create",
        json={
            "name": "line-test",
            "projectId": projectId,
        }
    )
    lineId = response.json["id"]
    return [projectId, lineId]
