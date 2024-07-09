from uuid import UUID
from ..errors.AppError import AppError
from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from ..models.CommandModel import CommandModel
from .WorkflowRepository import WorkflowRepository
from .CommandRepository import CommandRepository

workflowRepository = WorkflowRepository()
commandRepository = CommandRepository()


class DatasetRepository():

    def create(self, userId, workflowId) -> dict:
        user = UserModel.query.filter_by(id=UUID(userId)).first()
        dataset = DataSetModel(
            workflowId=workflowId,
            owner_email=user.email
        )
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        commands = CommandModel.query.filter_by(workflowId=workflowId).all()
        database.session.add(dataset)
        database.session.commit()

        newWorkflowData = {
            "name": workflow.name,
            "parentType": "datasetId",
        }

        workflowRepository.create(
            userId,
            newWorkflowData,
            dataset.id,
        )

        for command in commands:
            commandRepository.create(
                userId,
                workflowId,
                command.name,
                command.parameters
            )
            database.session.add(commands)

        database.session.add(workflow)
        database.session.commit()

        return dataset.getAttributes()

    def showById(self, id):
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)

        return dataset.getAttributes()

    def showAll(self, workflowId):
        datasets = DataSetModel.query.filter_by(workflowId=workflowId).all()
        if len(datasets) == 0:
            raise AppError("There are no datasets", 404)

        return [dataset.getAttributes() for dataset in datasets]

    def delete(self, id):
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)

        database.session.delete(dataset)
        database.session.commit()

        return dataset.getAttributes()
