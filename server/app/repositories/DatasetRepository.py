from typing import Dict

from sqlalchemy import UUID

from app.errors.AppError import AppError 

from ..database.connection import database
from ..models.DataSetModel import DataSet
from .WorkflowRepository import WorkflowRepository

# Fiz baseado no UserRepository
# Show, update, delete, post

workoflowRepository = WorkflowRepository()
class DatasetRepository():

    def create(self, projectId, workflowId) -> Dict:
        dataset = DataSet(projectId=projectId)
        workflow = DataSet.query.filter_by(id=workflowId).first()
        workoflowRepository.create({
            "name": "NEW NEWDATASET",
            "parent": {
                "parentId": dataset.id,
                "parentType": "datasetId"
            }
        })
        database.session.add(dataset)
        database.session.add(workflow)
        database.session.commit()
        return dataset.getAttributes()
    
    def showById(self, id) -> DataSet:
        dataset = DataSet.query.filter_by(id=UUID(id)).frist()
        if not dataset:
            raise AppError("Dataset does not exist", 404)
        return dataset.getAttributes()

    def showAll(self):
        datasets: list[DataSet] = DataSet.query.all()
        if not datasets:
            raise AppError("There are no datasets", 404)
        return [dataset.getAttributes() for dataset in datasets]
