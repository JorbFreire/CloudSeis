from flask import Blueprint, request, jsonify

from ...middlewares.decoratorsFactory import decorator_factory
from ...middlewares.validateRequestBody import validateRequestBody

from ...controllers import programGroupController
from ...errors.AppError import AppError
from ...serializers.ProgramGroupSerializer import ProgramGroupCreateSchema

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
@decorator_factory(validateRequestBody, SerializerSchema=ProgramGroupCreateSchema)
def createProgramGroup():
    data = request.get_json()

    newProgramGroup = programGroupController.create(data)
    return jsonify(newProgramGroup)


@programGroupRouter.route("/update", methods=['PUT'])
def updateProgramGroup():
    data = request.get_json()
    # ! not implemented 
    updatedProgramGroup = programGroupController.update()
    return jsonify(updatedProgramGroup)


@programGroupRouter.route("/delete/<groupId>", methods=['DELETE'])
def deleteProgram(groupId):
    programGroup = programGroupController.delete(groupId)
    return jsonify(programGroup)
