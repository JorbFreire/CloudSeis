from flask import Blueprint, request, jsonify

from ...repositories.ParameterRepository import ParameterRepository
from ...errors.AppError import AppError

parameterRouter = Blueprint(
    "program-parameter-routes",
    __name__,
    url_prefix="/programs/parameters"
)
parameterRepository = ParameterRepository()


@parameterRouter.route("/list/<programId>", methods=['GET'])
def listPrograms(programId):
    programs = parameterRepository.showByProgramId(programId)
    return jsonify(programs)


@parameterRouter.route("/create/<programId>", methods=['POST'])
def createProgram(programId):
    newParameter = parameterRepository.create(programId)
    return jsonify(newParameter)


@parameterRouter.route("/update/<parameterId>", methods=['PUT'])
def updateProgram(parameterId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedParameter = parameterRepository.update(parameterId, data)
    return jsonify(updatedParameter)


@parameterRouter.route("/delete/<parameterId>", methods=['DELETE'])
def deleteProgram(parameterId):
    parameter = parameterRepository.delete(parameterId)
    return jsonify(parameter)
