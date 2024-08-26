import pytest

DEFAULT_PASSWORD = "password123"

class Mock():
    client = pytest.client
    user = dict()
    project = dict()
    line = dict()
    workflow = dict()
    token: str = ""

    def createSession(self, email, password=DEFAULT_PASSWORD):
        response = self.client.post(
            "/session/",
            json={
                "email": email,
                "password": password
            }
        )
        return response.json["token"]

    def loadUser(self, name="root"):
        email = f'{name}@email.com'
        response = self.client.post(
            "/user/create",
            json={
                "name": name,
                "email": email,
                "password": DEFAULT_PASSWORD
            }
        )
        user_data = response.json
        self.user = user_data
        return user_data

    def loadSession(self):
        token = self.createSession(email=self.user["email"])
        self.token = token
        return token

    def loadProject(self):
        response = self.client.post(
            "/project/create",
            json={
                "name": "project_test",
                "userId": self.user["id"],
            },
            headers={
                "Authorization": self.token
            }
        )
        project_data = response.json
        self.project = project_data
        return project_data

    def loadLine(self):
        response = self.client.post(
            f"/line/create/{self.project['id']}",
            json={
                "name": "line_test",
                "projectId": self.project["id"],
            },
            headers={
                "Authorization": self.token
            }
        )
        line_data = response.json
        self.line = line_data
        return line_data

    def loadWorkflow(self):
        response = self.client.post(
            f"/workflow/create/{self.project['id']}",
            json={
                "name": "workflow_test",
                "parentType": "projectId"
            },
            headers={
                "Authorization": self.token
            }
        )
        workflow_data = response.json
        self.workflow = workflow_data
        return workflow_data
