from flask import Blueprint, request, jsonify

from ..models.WorkflowModel import WorkflowModel
from ..repositories.WorkflowRepository import WorkflowRepository
from ..errors.AppError import AppError

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication

workflowRouter = Blueprint(
    "workflow-routes",
    __name__,
    url_prefix="/workflow"
)
workflowRepository = WorkflowRepository()


@workflowRouter.route("/show", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showWorkflow(userId, id):
    workflow = workflowRepository.showById(id)
    return jsonify(workflow)


@workflowRouter.route("/create", methods=['POST'])
@decorator_factory(requireAuthentication)
def createWorkflow(userId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newWorkflow = workflowRepository.create(userId, data)
    return jsonify(newWorkflow)


@workflowRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(userId, id):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedWorkflow = workflowRepository.update(
        # id,
        # data
    )
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def deleteWorkflow(userId, id):
    workflow = workflowRepository.delete(id)
    return jsonify(workflow)
