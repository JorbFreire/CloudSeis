from uuid import UUID
from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.WorkflowModel import WorkflowModel
from ..models.FileLinkModel import FileLinkModel

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

    def create(self, userId, newWorkflowData, parentId):
        parentType = newWorkflowData["parentType"]

        user = UserModel.query.filter_by(id=UUID(userId)).first()
        if not user:
            raise AppError("User does not exist", 404)

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

        newWorkflow = WorkflowModel(
            name=newWorkflowData["name"],
            owner_email=user.email,
        )

        database.session.add(newWorkflow)
        database.session.commit()

        newWorkflowId = newWorkflow.id
        workflowParentsAssociationRepository.create(
            newWorkflowId,
            parentType,
            parentId
        )
        orderedCommandsListRepository.create(newWorkflow.id)

        return newWorkflow.getAttributes()

    def updateName(self, userId, data):
        raise AppError("Not implemented")

    def updateFilePath(self, workflowId, fileLinkId):
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        fileLink = FileLinkModel.query.filter_by(id=fileLinkId).first()
        if not fileLink:
            raise AppError("FileLink does not exist", 404)

        workflow.file_link_id = fileLink.id

        database.session.commit()
        return workflow.getAttributes()

    def delete(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        database.session.delete(workflow)
        database.session.commit()
        return workflow.getAttributes()
