from ..database.connection import database
from ..models.WorkflowModel import WorkflowModel

from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel
from ..models.DataSetModel import DataSetModel

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
        parentType = newWorkflowData["parent"]["parentType"]
        parentId = newWorkflowData["parent"]["parentId"]

        if parentType == "lineId":
            parent = LineModel.query.filter_by(id=parentId).first()
            if not parent:
                raise AppError("Line does not exist", 404)
        elif parentType == "projectId":
            parent = ProjectModel.query.filter_by(id=parentId).first()
            if not parent:
                raise AppError("Project does not exist", 404)
        elif parentType == "datasetId":
            parent = DataSetModel.query.filter_by(id=parentId).first()
            if not parent:
                raise AppError("DataSet does not exist", 404)
        else:
            raise AppError(
                "'parentType' must be either 'lineId', 'projectId' or 'datasetId'"
            )

        newWorkflow = WorkflowModel(
            name=newWorkflowData["name"],
            file_name=""
        )
        database.session.add(newWorkflow)
        database.session.commit()

        newWorkflowId = newWorkflow.id
        workflowParentsAssociationRepository.create(
            newWorkflowId,
            newWorkflowData["parent"]
        )
        orderedCommandsListRepository.create(newWorkflow.id)

        return newWorkflow.getAttributes()

    def delete(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        database.session.delete(workflow)
        database.session.commit()
        return workflow.getAttributes()
