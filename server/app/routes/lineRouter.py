from flask import Blueprint, request, jsonify


from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication

from ..models.LineModel import LineModel
from ..repositories.LineRepository import LineRepository

lineRouter = Blueprint(
    "line-routes",
    __name__,
    url_prefix="/line"
)
lineRepository = LineRepository()


@lineRouter.route("/list/<projectId>", methods=['GET'])
def showLine(projectId):
    line = lineRepository.showByProjectId(projectId)
    return jsonify(line)


@lineRouter.route("/create", methods=['POST'])
@decorator_factory(requireAuthentication) # Line creation depends on ProjectModel
def createLine(userId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    elif "name" not in data or "projectId" not in data:
        return jsonify(
            {"Error": "Invalid body"},
            status=400
        )
    newLine = lineRepository.create(
        userId,
        data["projectId"],
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update", methods=['PUT'])
@decorator_factory(requireAuthentication, routeModel=LineModel)
def updateLine(userId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    updatedLine = lineRepository.update(
        data["lineId"], data["name"]
    )
    return jsonify(updatedLine)


@lineRouter.route("/delete", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=LineModel)
def deleteLine(userId):
    data = request.get_json()
    line = lineRepository.delete(data["lineId"])
    return jsonify(line)
