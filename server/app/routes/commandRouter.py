from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..repositories.CommandRepository import CommandRepository
from ..repositories.OrderedCommandsListRepository import OrderedCommandsListRepository
from ..serializers.CommandSerializer import CommandShowtSchema, CommandCreateSchema, CommandUpdateParametersSchema, CommandsUpdateOrderSchema, CommandDeleteSchema
from ..models.CommandModel import CommandModel


commandRouter = Blueprint(
    "command-routes",
    __name__,
    url_prefix="/command"
)
commandRepository = CommandRepository()
orderedCommandsListRepository = OrderedCommandsListRepository()


@commandRouter.route("/show/<id>", methods=['GET'])
# @decorator_factory(validateRequestBody, SerializerSchema=CommandShowtSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def showCommand(_, id):
    command = commandRepository.show(id)
    return jsonify(command)


@commandRouter.route("/create/<workflowId>", methods=['POST'])
# @decorator_factory(validateRequestBody, SerializerSchema=CommandCreateSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def createCommand(userId, workflowId):
    data = request.get_json()
    newCommand = commandRepository.create(
        userId,
        workflowId,
        data["name"],
        data["parameters"]
    )
    return jsonify(newCommand)


@commandRouter.route("/update/<id>", methods=['PUT'])
# @decorator_factory(validateRequestBody, SerializerSchema=CommandUpdateParametersSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def updateCommand(_, id):
    data = request.get_json()
    updatedCommand = commandRepository.updateParameters(
        id,
        data["parameters"]
    )
    return jsonify(updatedCommand)


@commandRouter.route("/order/<workflowId>", methods=['PUT'])
# @decorator_factory(validateRequestBody, SerializerSchema=CommandsUpdateOrderSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def updateOrder(_, workflowId):
    data = request.get_json()
    updatedCommandList = orderedCommandsListRepository.update(
        workflowId,
        data["newOrder"]
    )
    return jsonify(updatedCommandList)


@commandRouter.route("/delete/<id>", methods=['DELETE'])
# @decorator_factory(validateRequestBody, SerializerSchema=CommandDeleteSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def deleteCommand(_, id):
    command = commandRepository.delete(id)
    return jsonify(command)
