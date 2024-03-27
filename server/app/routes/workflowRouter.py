from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..serializers.WorkflowSerializer import WorkflowShowSchema, WorkflowCreateSchema, WorkflowUpdateSchema, WorkflowDeleteSchema
from ..repositories.WorkflowRepository import WorkflowRepository

workflowRouter = Blueprint(
    "workflow-routes",
    __name__,
    url_prefix="/workflow"
)
workflowRepository = WorkflowRepository()


@workflowRouter.route("/show/<id>", methods=['GET'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowShowSchema)
@decorator_factory(requireAuthentication)
def showWorkflow(_, id):
    workflow = workflowRepository.showById(id)
    return jsonify(workflow)


@workflowRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowCreateSchema)
@decorator_factory(requireAuthentication)
def createWorkflow():
    data = request.get_json()
    newWorkflow = workflowRepository.create(data)
    return jsonify(newWorkflow)


@workflowRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowUpdateSchema)
@decorator_factory(requireAuthentication)
def updateWorkflow(id):
    data = request.get_json()
    updatedWorkflow = workflowRepository.updateName(
        id,
        data
    )
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowDeleteSchema)
@decorator_factory(requireAuthentication)
def deleteWorkflow(id):
    workflow = workflowRepository.delete(id)
    return jsonify(workflow)
