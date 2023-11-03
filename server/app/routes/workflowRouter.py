from flask import Blueprint, request, jsonify

from ..repositories.WorkflowRepository import WorkflowRepository
from ..errors.AppError import AppError

workflowRouter = Blueprint(
    "workflow-routes",
    __name__,
    url_prefix="/workflow"
)
workflowRepository = WorkflowRepository()


@workflowRouter.route("/show/<id>", methods=['GET'])
def showWorkflow(id):
    workflow = workflowRepository.showById(id)
    return jsonify(workflow)


@workflowRouter.route("/create", methods=['POST'])
def createWorkflow():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newWorkflow = workflowRepository.create(data)
    return jsonify(newWorkflow)


@workflowRouter.route("/update/<id>", methods=['PUT'])
def updateWorkflow(id):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedWorkflow = workflowRepository.updateName(
        id,
        data
    )
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
def deleteWorkflow(id):
    workflow = workflowRepository.delete(id)
    return jsonify(workflow)
