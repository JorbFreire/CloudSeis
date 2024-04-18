from flask import Blueprint, request, jsonify

from ...repositories.ProgramGroupRepository import ProgramGroupRepository
from ...errors.AppError import AppError

programGroupRouter = Blueprint(
    "programs-groups-routes",
    __name__,
    url_prefix="/programs/groups"
)
programGroupRepository = ProgramGroupRepository()


@programGroupRouter.route("/list", methods=['GET'])
def listGroups():
    program_groups = programGroupRepository.listAll()
    return jsonify(program_groups)


@programGroupRouter.route("/create", methods=['POST'])
def createProgramGroup():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newProgramGroup = programGroupRepository.create(data)
    return jsonify(newProgramGroup)


@programGroupRouter.route("/update", methods=['PUT'])
def updateProgramGroup():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedProgramGroup = programGroupRepository.update()
    return jsonify(updatedProgramGroup)


@programGroupRouter.route("/delete/<groupId>", methods=['DELETE'])
def deleteProgram(groupId):
    programGroup = programGroupRepository.delete(groupId)
    return jsonify(programGroup)
