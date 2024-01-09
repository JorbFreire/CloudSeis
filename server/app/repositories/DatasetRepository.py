from typing import Dict

from sqlalchemy import UUID

from ..errors.AppError import AppError
from ..database.connection import database
from ..models.DataSetModel import DataSet
from ..models.WorkflowModel import WorkflowModel
from .WorkflowRepository import WorkflowRepository

# Fiz baseado no UserRepository
# Show, update, delete, post

workflowRepository = WorkflowRepository()
class DatasetRepository():

    def create(self, projectId, workflowId) -> Dict:
        dataset = DataSet()
        dataset.projectId = projectId
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        workflowRepository.create({
            "name": "NEW NEWDATASET",
            "parent": {
                "parentId": dataset.id,
                "parentType": "datasetId"
            }
        })
        database.session.add(dataset)
        database.session.add(workflow) # Reclamou aq
#     raise exc.UnmappedInstanceError(instance) from err
# sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.NoneType' is not mapped
        database.session.commit()
        return dataset.getAttributes()
    
    def showById(self, id) -> DataSet:
        dataset = DataSet.query.filter_by(id=id).first()
        if not dataset:
            raise AppError("Dataset does not exist", 404)
        return dataset.getAttributes()

    def showAll(self):
        datasets: list[DataSet] = DataSet.query.all()
        if not datasets:
            raise AppError("There are no datasets", 404)
        return [dataset.getAttributes() for dataset in datasets]
