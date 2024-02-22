from flask import Blueprint, request, jsonify

from ..repositories.ProgramRepository import ProgramRepository
from ..errors.AppError import AppError

programRouter = Blueprint("program-routes", __name__, url_prefix="/programs")
programRepository = ProgramRepository()


@programRouter.route("/list/<groupId>", methods=['GET'])
def listPrograms(groupId):
    programs = programRepository.showByGroupId(groupId)
    return jsonify(programs)


@programRouter.route("/create/<groupId>", methods=['POST'])
def createProgram(groupId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newProgram = programRepository.create(groupId, data)
    return jsonify(newProgram)


@programRouter.route("/update/<programId>", methods=['PUT'])
def updateProgram(programId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedProgram = programRepository.update(programId, data)
    return jsonify(updatedProgram)


@programRouter.route("/delete/<programId>", methods=['DELETE'])
def deleteProgram(programId):
    program = programRepository.delete(programId)
    return jsonify(program)
