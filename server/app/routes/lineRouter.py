from flask import Blueprint, request, jsonify

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
def createLine():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    newLine = lineRepository.create(
        data["projectId"],
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update", methods=['PUT'])
def updateLine(lineId):
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


@lineRouter.route("/delete/<id>", methods=['DELETE'])
def deleteLine(id):
    line = lineRepository.delete(id)
    return jsonify(line)
