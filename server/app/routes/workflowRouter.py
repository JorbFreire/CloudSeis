from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..serializers.WorkflowSerializer import WorkflowShowSchema, WorkflowCreateSchema, WorkflowUpdateSchema, WorkflowDeleteSchema
from ..repositories.WorkflowRepository import WorkflowRepository
from ..models.WorkflowModel import WorkflowModel

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication

workflowRouter = Blueprint(
    "workflow-routes",
    __name__,
    url_prefix="/workflow"
)
workflowRepository = WorkflowRepository()


@workflowRouter.route("/show/<id>", methods=['GET'])
# @decorator_factory(validateRequestBody, SerializerSchema=WorkflowShowSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showWorkflow(_, id):
    workflow = workflowRepository.showById(id)
    return jsonify(workflow)


@workflowRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowCreateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def createWorkflow(userId):
    data = request.get_json()
    newWorkflow = workflowRepository.create(userId, data)
    return jsonify(newWorkflow)


@workflowRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(userId):
    data = request.get_json()
    updatedWorkflow = workflowRepository.updateName(
        # ! not implemented
        # userId,
        # data
    )
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
# @decorator_factory(validateRequestBody, SerializerSchema=WorkflowDeleteSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def deleteWorkflow(_, id):
    workflow = workflowRepository.delete(id)
    return jsonify(workflow)
