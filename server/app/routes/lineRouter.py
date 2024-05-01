from flask import Blueprint, request, jsonify


from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..models.LineModel import LineModel
from ..models.ProjectModel import ProjectModel
from ..repositories.LineRepository import LineRepository
from ..serializers.LineSerializer import LineCreateSchema, LineUpdateSchema

lineRouter = Blueprint(
    "line-routes",
    __name__,
    url_prefix="/line"
)
lineRepository = LineRepository()


@lineRouter.route("/list/<projectId>", methods=['GET'])
@decorator_factory(requireAuthentication)
def listLines(_, projectId):
    lines = lineRepository.showByProjectId(projectId)
    return jsonify(lines)


@lineRouter.route("/create/<projectId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=LineCreateSchema)
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createLine(userId, projectId):
    data = request.get_json()
    newLine = lineRepository.create(
        userId,
        projectId,
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update/<lineId>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=LineUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=LineModel)
def updateLine(_, lineId):
    data = request.get_json()
    updatedLine = lineRepository.update(
        lineId,
        data["name"]
    )
    return jsonify(updatedLine)


@lineRouter.route("/delete/<lineId>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=LineModel)
def deleteLine(_, lineId):
    line = lineRepository.delete(lineId)
    return jsonify(line)

# DEBUG ROUTE


@lineRouter.route("/listall/debug", methods=['GET'])
def listall():
    lines = lineRepository.listAllDebug()
    return jsonify(lines)
