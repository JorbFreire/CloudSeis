import pytest
from icecream import ic
# ! any of this function cant be NEVER used twice with the same args !


def get_test_user_data(name="root"):
    name = f'user_{name}'
    email = f'{name}@email.com'
    response = pytest.client.post(
        "/user/test",
        json={
            "name": name,
            "email": email,
            "password": "password123"
        }
    )
    user_data = response.json
    return user_data


def get_test_user_session(name="root"):
    email = f'{name}@email.com'
    response = pytest.client.post(
        "/session/",
        json = {
            "email": email,
            "password": "password123"
        }
    )
    return response.json


def get_test_project_data(name="project"):
    user_data = get_test_user_data(name=name)
    token = get_test_user_session(name=user_data["name"])
    response = pytest.client.post(
        "/project/create",
        json={
            "name": "project_test",
            "userId": user_data["id"],
        },
        headers = {
            "Authorization": token
        }
    )
    project_data = response.json
    return project_data, user_data


def get_test_line_data(name="line"):
    project_data, user_data = get_test_project_data(name=name)
    token = get_test_user_session(name=user_data["name"])
    response = pytest.client.post(
        f"/line/create/{project_data['id']}",
        json={
            "name": "line_test",
            "projectId": project_data["id"],
        },
        headers = {
            "Authorization": token
        }
    )
    line_data = response.json
    return line_data, project_data, user_data

def get_test_workflow_data(name="workflow"):
    line_data, project_data, user_data = get_test_line_data(name=name)
    token = get_test_user_session(name=user_data["name"])
    response = pytest.client.post(
        f"/workflow/create/{line_data['id']}",
        json = {
            "name": "workflow_test",
            "parentType": "lineId" 
        }, 
        headers = {
            "Authorization": token
        }
    )
    workflow_data = response.json
    return workflow_data, line_data, project_data, user_data
