from types import SimpleNamespace

from ..database.connection import database
from ..models.WorkflowModel import WorkflowModel

from ..errors.AppError import AppError
from ..repositories.WorkflowRepository import workflowRepository
from ..repositories.WorkflowParentsAssociationRepository import workflowParentsAssociationRepository
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository


def showById(id):
    workflow = WorkflowModel.query.filter_by(id=id).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    return workflow.getAttributes()


def create(userId, newWorkflowData, parentId):
    newWorkflow = workflowRepository.create(userId, newWorkflowData, parentId)

    workflowParentsAssociationRepository.create(
        newWorkflow.id,
        newWorkflowData["parentType"],
        parentId
    )
    orderedCommandsListRepository.create(newWorkflow.id)

    return newWorkflow.getAttributes()


def updateName(userId, data):
    # ! breaks MVC !
    # ! not implemented
    raise AppError("Not implemented")


def updateFilePath(workflowId, fileLinkId):
    # ! breaks MVC !
    workflow = workflowRepository.updateFilePath(workflowId, fileLinkId)
    return workflow.getAttributes()


def delete(id):
    workflow = WorkflowModel.query.filter_by(id=id).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    database.session.delete(workflow)
    database.session.commit()
    return workflow.getAttributes()


workflowController = SimpleNamespace(
    showById=showById,
    create=create,
    updateName=updateName,
    updateFilePath=updateFilePath,
    delete=delete,
)
