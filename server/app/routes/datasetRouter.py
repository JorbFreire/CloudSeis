from flask import Blueprint, request, jsonify

from ..repositories.DatasetRepository import DatasetRepository
from ..repositories.WorkflowRepository import WorkflowRepository
from ..errors.AppError import AppError

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")
datasetRepository = DatasetRepository()

@datasetRouter.route("/list", methods=['GET'])
def listDatasets():
    datasets = datasetRepository.showAll()
    return jsonify(datasets)

@datasetRouter.route("/show/<datasetId>", methods=['GET'])
def showDataset(datasetId):
    dataset = datasetRepository.showById(datasetId)
    return jsonify(dataset)

@datasetRouter.route("/show/<datasetId>", methods=['POST'])
def createDataset():
    newDataset = DatasetRepository.create()
    # data = request.get_json()
    # if data is None:
    #     raise AppError("No body", 404)
    # newDataset = datasetRepository.create(data, projectiId, workflowId)
    return jsonify(newDataset)
