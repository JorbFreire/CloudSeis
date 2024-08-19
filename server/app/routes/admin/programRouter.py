from flask import Blueprint, request, jsonify

from ...middlewares.decoratorsFactory import decorator_factory
from ...middlewares.validateRequestBody import validateRequestBody

from ...controllers import programController
from ...errors.AppError import AppError
from ...serializers.ProgramSerializer import ProgramCreateSchema

programRouter = Blueprint("program-routes", __name__, url_prefix="/programs")


@programRouter.route("/list/<groupId>", methods=['GET'])
def listPrograms(groupId):
    programs = programController.showByGroupId(groupId)
    return jsonify(programs)


@programRouter.route("/create/<groupId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=ProgramCreateSchema)
def createProgram(groupId):
    data = request.form
    if data == None:
        raise AppError("No body", 400)

    newProgram = programController.create(groupId, data)
    return jsonify(newProgram)


@programRouter.route("/update/<programId>", methods=['PUT'])
def updateProgram(programId):
    data = request.form
    if data == None:
        raise AppError("No body", 400)

    updatedProgram = programController.update(programId, data)
    return jsonify(updatedProgram)


@programRouter.route("/delete/<programId>", methods=['DELETE'])
def deleteProgram(programId):
    program = programController.delete(programId)
    return jsonify(program)
