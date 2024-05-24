from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..repositories.ProjectRepository import ProjectRepository
from ..serializers.ProjectSerializer import ProjectCreateSchema, ProjectUpdateSchema
from ..models.ProjectModel import ProjectModel

projectRouter = Blueprint(
    "project-routes",
    __name__,
    url_prefix="/project"
)
projectRepository = ProjectRepository()


@projectRouter.route("/list", methods=['GET'])
@decorator_factory(requireAuthentication)
def showProject(userId):
    project = projectRepository.showByUserId(userId)
    return jsonify(project)


@projectRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=ProjectCreateSchema)
@decorator_factory(requireAuthentication)
def createProject(userId):
    data = request.get_json()
    newProject = projectRepository.create(userId, data["name"])
    return jsonify(newProject)


@projectRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=ProjectUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def updateProject(_, id):
    data = request.get_json()
    updatedProject = projectRepository.updateName(id, data["name"])
    return jsonify(updatedProject)


@projectRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def deleteProject(_, id):
    project = projectRepository.delete(id)
    return jsonify(project)


# * It does not include workflows inside lines
@projectRouter.route("/root-workflows/list/<id>", methods=['GET'])
@decorator_factory(requireAuthentication)
def listProjectRootWorkflows(_, id):
    projectWorkflows = projectRepository.listWorkflowsByProjectId(id)
    return jsonify(projectWorkflows)
