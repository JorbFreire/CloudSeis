from ..errors.AppError import AppError
from ..database.connection import database
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from ..models.CommandModel import CommandModel
from .WorkflowRepository import WorkflowRepository
from .CommandRepository import CommandRepository

workflowRepository = WorkflowRepository()
commandRepository = CommandRepository()


class DatasetRepository():

    def create(self, projectId, workflowId) -> dict:
        raise AppError("Fix for workflow adaptation")
        dataset = DataSetModel(
            projectId=projectId
        )
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        commands = CommandModel.query.filter_by(workflowId=workflowId).all()
        database.session.add(dataset)
        database.session.commit()

        workflowRepository.create({
            user.id,
            projectId
        })

        for command in commands:
            commandRepository.create(
                workflowId,
                command.name,
                command.parameters
            )
            database.session.add(commands)

        database.session.add(workflow)
        database.session.commit()

        return dataset.getAttributes()

    def showById(self, id):
        raise AppError("Adapt creation first")
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)

        return dataset.getAttributes()

    def showAll(self):
        datasets: list[DataSetModel] = DataSetModel.query.all()
        if not datasets:
            raise AppError("There are no datasets", 404)

        return [dataset.getAttributes() for dataset in datasets]

    def delete(self, id):
        raise AppError("Adapt creation first")
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)

        database.session.delete(dataset)
        database.session.commit()

        return dataset.getAttributes()
