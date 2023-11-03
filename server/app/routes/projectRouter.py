from flask import Blueprint, request, jsonify

from ..repositories.ProjectRepository import ProjectRepository

projectRouter = Blueprint(
    "project-routes",
    __name__,
    url_prefix="/project"
)
projectRepository = ProjectRepository()


@projectRouter.route("/list/<userId>", methods=['GET'])
def showProject(userId):
    project = projectRepository.showByUserId(userId)
    return jsonify(project)


@projectRouter.route("/create", methods=['POST'])
def createProject():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    newProject = projectRepository.create(data["userId"], data["name"])
    return jsonify(newProject)


@projectRouter.route("/update/<id>", methods=['PUT'])
def updateProject(id):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    updatedProject = projectRepository.updateName(id, data["name"])
    return jsonify(updatedProject)


@projectRouter.route("/delete/<id>", methods=['DELETE'])
def deleteProject(id):
    project = projectRepository.delete(id)
    return jsonify(project)


# * It does not include workflows inside lines
@projectRouter.route("/root-workflows/list/<id>", methods=['GET'])
def listProjectRootWorkflows(id):
    projectWorkflows = projectRepository.listWorkflowsByProjectId(id)
    return jsonify(projectWorkflows)
