from ..database.connection import database
from ..models.WorkflowModel import WorkflowModel
from ..errors.AppError import AppError
from ..repositories.OrderedCommandsListRepository import OrderedCommandsListRepository
from ..repositories.WorkflowParentsAssociationRepository import WorkflowParentsAssociationRepository


workflowParentsAssociationRepository = WorkflowParentsAssociationRepository()
orderedCommandsListRepository = OrderedCommandsListRepository()


class WorkflowRepository:
    def showById(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        return workflow.getAttributes()

    def create(self, newWorkflowData):
        newWorkflow = WorkflowModel({
            "name": newWorkflowData["name"],
            "file_name": ""
        })
        database.session.add(newWorkflow)
        database.session.commit()
        
        workflowParentsAssociationRepository.create(
            newWorkflow["id"],
            newWorkflow["parent"]
        )
        orderedCommandsListRepository.create(newWorkflow.id)

        return newWorkflow.getAttributes()

    def updateName(self, id, newWorkflowName):
        pass

    def delete(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        database.session.delete(workflow)
        database.session.commit()
        return workflow.getAttributes()
