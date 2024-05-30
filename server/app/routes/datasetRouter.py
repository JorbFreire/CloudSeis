from flask import Blueprint, request, jsonify

from ..models.WorkflowModel import WorkflowModel

from ..models.DataSetModel import DataSetModel

from ..repositories.DatasetRepository import DatasetRepository

from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.decoratorsFactory import decorator_factory

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")
datasetRepository = DatasetRepository()


# todo: final version should not get a "create" route for dataset
# todo: datasets should be created when running plot

@datasetRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=DataSetModel)
def deleteDataset(_, id):
    dataset = datasetRepository.delete(id)
    return jsonify(dataset)


@datasetRouter.route("/show/<id>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=DataSetModel)
def showDataset(_, id):
    dataset = datasetRepository.showById(id)
    return jsonify(dataset)


# Debug route probably
@datasetRouter.route("/list", methods=['GET'])
def listDatasets():
    datasets = datasetRepository.showAll()
    return jsonify(datasets)
