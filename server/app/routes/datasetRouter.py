from flask import Blueprint, jsonify

from ..models.DataSetModel import DataSetModel
from ..repositories.DatasetRepository import DatasetRepository
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.decoratorsFactory import decorator_factory

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")
datasetRepository = DatasetRepository()

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


@datasetRouter.route("/list/<workflowId>", methods=['GET'])
# @decorator_factory(requireAuthentication, routeModel=DataSetModel)
def listDatasets(workflowId):
    datasets = datasetRepository.showAll(workflowId)
    return jsonify(datasets)
