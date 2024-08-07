from uuid import UUID
from types import SimpleNamespace

from ..errors.AppError import AppError
from ..database.connection import database

from ..models.UserModel import UserModel
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from ..models.CommandModel import CommandModel

from ..repositories.WorkflowRepository import workflowRepository
from ..repositories.CommandRepository import commandRepository


def showById(id):
    dataset = DataSetModel.query.filter_by(id=id).first()
    if not dataset:
        raise AppError("Dataset does not exist", 404)

    return dataset.getAttributes()


def showAll(workflowId):
    datasets = DataSetModel.query.filter_by(workflowId=workflowId).all()
    if len(datasets) == 0:
        raise AppError("There are no datasets", 404)

    return [dataset.getAttributes() for dataset in datasets]


def delete(id):
    dataset = DataSetModel.query.filter_by(id=id).first()
    if not dataset:
        raise AppError("Dataset does not exist", 404)

    database.session.delete(dataset)
    database.session.commit()

    return dataset.getAttributes()


datasetController = SimpleNamespace(
    showById=showById,
    showAll=showAll,
    delete=delete,
)
