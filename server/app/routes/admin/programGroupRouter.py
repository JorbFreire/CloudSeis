from flask import Blueprint, request, jsonify

from ...controllers import programGroupController
from ...errors.AppError import AppError

programGroupRouter = Blueprint(
    "programs-groups-routes",
    __name__,
    url_prefix="/programs/groups"
)


@programGroupRouter.route("/list", methods=['GET'])
def listGroups():
    program_groups = programGroupController.listAll()
    return jsonify(program_groups)


@programGroupRouter.route("/create", methods=['POST'])
def createProgramGroup():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newProgramGroup = programGroupController.create(data)
    return jsonify(newProgramGroup)


@programGroupRouter.route("/update", methods=['PUT'])
def updateProgramGroup():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedProgramGroup = programGroupController.update()
    return jsonify(updatedProgramGroup)


@programGroupRouter.route("/delete/<groupId>", methods=['DELETE'])
def deleteProgram(groupId):
    programGroup = programGroupController.delete(groupId)
    return jsonify(programGroup)
