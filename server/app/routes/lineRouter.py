from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..repositories.LineRepository import LineRepository
from ..serializers.LineSerializer import LineListSchema, LineCreateSchema

lineRouter = Blueprint(
    "line-routes",
    __name__,
    url_prefix="/line"
)
lineRepository = LineRepository()


@lineRouter.route("/list/<projectId>", methods=['GET'])
@decorator_factory(validateRequestBody, SerializerSchema=LineListSchema)
@decorator_factory(requireAuthentication)
def showLine(userId, projectId):
    line = lineRepository.showByProjectId(projectId)
    return jsonify(line)


@lineRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=LineCreateSchema)
@decorator_factory(requireAuthentication)
def createLine(userId):
    data = request.get_json()
    newLine = lineRepository.create(
        data["projectId"],
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update/<lineId>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=LineCreateSchema)
@decorator_factory(requireAuthentication)
def updateLine(userId, lineId):
    data = request.get_json()
    updatedLine = lineRepository.update(
        lineId,
        data["name"]
    )
    return jsonify(updatedLine)


@lineRouter.route("/delete/<lineId>", methods=['DELETE'])
@decorator_factory(validateRequestBody, SerializerSchema=LineCreateSchema)
@decorator_factory(requireAuthentication)
def deleteLine(userId, lineId):
    line = lineRepository.delete(lineId)
    return jsonify(line)
