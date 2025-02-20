import pytest
from os import path

DEFAULT_PASSWORD = "password123"

class Mock():
    client = pytest.client
    base_marmousi_stack_path = path.join(
        path.dirname(__file__),
        "mock_seismic_data",
        "marmousi_4ms_stack.su"
    )
    user = dict()
    project = dict()
    line = dict()
    workflow = dict()
    # *** valid sufilter command
    sufilterCommand = dict()

    programGroup = dict()
    program = dict()
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
    
    def loadProgramGroup(self):
        response = self.client.post(
            f"/programs/groups/create",
            json={
                "name": "program_test",
                "description": "no description"
            },
            headers={
                "Authorization": self.token,
            }
        )
        programGroupData = response.json
        self.programGroup = programGroupData
        return programGroupData
    
    def loadProgram(
        self,
        name="program_test",
        description="no description",
    ):
        response = self.client.post(
            f"/programs/create/{self.programGroup['id']}",
            data={
                "name": name,
                "description": description,
                "path_to_executable_file": name,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded", 
                "Authorization": self.token,
            }
        )
        programData = response.json
        self.program = programData
        return programData

    def loadSufilterCommand(self):
        # *** load valid sufilter program
        # *** load valid command with valid paremeters for sufilter
        self.loadProgram(
            name="sufilter",
            description="applies a zero-phase, sine-squared tapered filter"
        )
        parameters = {
            "f": "10, 20, 150, 200",
            "amps": "0, 1, 1, 0"
        }
        response = self.client.post(
            f"/dataset/create/{self.workflow['id']}",
            json={
                "name": "sufilter",
                "parameters": parameters,
                "program_id": self.program['id'],
            },
            headers={
                "Authorization": self.token
            }
        )
        commandData = response.json
        self.sufilterCommand = commandData
        return commandData
