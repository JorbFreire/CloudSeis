from flask import Blueprint, request, jsonify

from ..repositories.ProgramRepository import ProgramRepository
from ..repositories.ProgramFileRepository import ProgramFileRepository
from ..errors.AppError import AppError

programRouter = Blueprint("program-routes", __name__, url_prefix="/programs")
programRepository = ProgramRepository()
programFileRepository = ProgramFileRepository()


@programRouter.route("/list/<groupId>", methods=['GET'])
def listPrograms(groupId):
    programs = programRepository.showByGroupId(groupId)
    return jsonify(programs)


@programRouter.route("/create/<groupId>", methods=['POST'])
def createProgram(groupId):
    data = request.form
    if data == None:
        raise AppError("No body", 400)

    if ('file' in request.files):
        file = request.files['file']
        unique_filename = programFileRepository.create(file)
        data["path_to_executable_file"] = unique_filename

    newProgram = programRepository.create(groupId, data)
    return jsonify(newProgram)


@programRouter.route("/update/<programId>", methods=['PUT'])
def updateProgram(programId):
    data = request.form
    if data == None:
        raise AppError("No body", 400)

    if ('file' in request.files):
        file = request.files['file']
        unique_filename = programFileRepository.create(file)
        data["path_to_executable_file"] = unique_filename

    updatedProgram = programRepository.update(programId, data)
    return jsonify(updatedProgram)


@programRouter.route("/delete/<programId>", methods=['DELETE'])
def deleteProgram(programId):
    program = programRepository.delete(programId)
    return jsonify(program)
