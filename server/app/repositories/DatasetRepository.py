from ..errors.AppError import AppError
from ..database.connection import database
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from .WorkflowRepository import WorkflowRepository

workflowRepository = WorkflowRepository()


class DatasetRepository():

    def create(self, projectId, workflowId) -> dict:
        dataset = DataSetModel(
            projectId=projectId
        )
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        database.session.add(dataset)
        database.session.commit()

        workflowRepository.create({
            "name": "NEW NEWDATASET",
            "parent": {
                "parentId": dataset.id,
                "parentType": "datasetId"
            }
        })
        database.session.add(workflow)
        database.session.commit()
        return dataset.getAttributes()

    def showById(self, id):
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)
        return dataset.getAttributes()

    def showAll(self):
        datasets: list[DataSetModel] = DataSetModel.query.all()
        if not datasets:
            raise AppError("There are no datasets", 404)
        return [dataset.getAttributes() for dataset in datasets]

    def delete(self):
        dataset = DataSetModel.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)

        database.session.delete(dataset)
        database.session.commit()
        return dataset.getAttributes
