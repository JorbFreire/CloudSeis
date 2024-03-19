from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication

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
@decorator_factory("DELETE", requireAuthentication)
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
        data["projectId"],
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update", methods=['PUT'])
@decorator_factory("DELETE", requireAuthentication)
def updateLine(userId, lineId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    updatedLine = lineRepository.update(
        lineId, data["name"]
    )
    return jsonify(updatedLine)


@lineRouter.route("/delete/<lineId>", methods=['DELETE'])
@decorator_factory("DELETE", requireAuthentication)
def deleteLine(userId, lineId):
    line = lineRepository.delete(lineId)
    return jsonify(line)
