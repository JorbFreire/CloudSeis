from flask import Blueprint, request, jsonify

from ...controllers.admin import parameterController
from ...errors.AppError import AppError

parameterRouter = Blueprint(
    "program-parameter-routes",
    __name__,
    url_prefix="/programs/parameters"
)


@parameterRouter.route("/list/<programId>", methods=['GET'])
def listPrograms(programId):
    programs = parameterController.showByProgramId(programId)
    return jsonify(programs)


@parameterRouter.route("/create/<programId>", methods=['POST'])
def createProgram(programId):
    newParameter = parameterController.create(programId)
    return jsonify(newParameter)


@parameterRouter.route("/update/<parameterId>", methods=['PUT'])
def updateProgram(parameterId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedParameter = parameterController.update(parameterId, data)
    return jsonify(updatedParameter)


@parameterRouter.route("/delete/<parameterId>", methods=['DELETE'])
def deleteProgram(parameterId):
    parameter = parameterController.delete(parameterId)
    return jsonify(parameter)
