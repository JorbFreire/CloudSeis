from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..serializers.WorkflowSerializer import WorkflowCreateSchema, WorkflowUpdateSchema
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
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showWorkflow(_, id):
    workflow = workflowRepository.showById(id)
    return jsonify(workflow)


# *** shall have an line id or project id the route params
@workflowRouter.route("/create/<parentId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowCreateSchema)
@decorator_factory(requireAuthentication)
def createWorkflow(userId, parentId):
    data = request.get_json()
    newWorkflow = workflowRepository.create(userId, data, parentId)
    return jsonify(newWorkflow)


@workflowRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(_, id):
    data = request.get_json()
    updatedWorkflow = workflowRepository.updateName(id, data)
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def deleteWorkflow(_, id):
    workflow = workflowRepository.delete(id)
    return jsonify(workflow)
