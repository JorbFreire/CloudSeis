from flask import Blueprint, request, jsonify

from ..repositories.DatasetRepository import DatasetRepository
from ..errors.AppError import AppError

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")
datasetRepository = DatasetRepository()


@datasetRouter.route("/create", methods=['POST'])
# todo: final version should not get a "create" route for dataset
# todo: datasets should be created when running plot
def createDataset():
    data = request.get_json()
    if data is None:
        raise AppError("No body", 400)
    elif "projectId" not in data or "workflowId" not in data:
        raise AppError("Ivalid Body", 400)  # Not sure if its 400 error
    newDataset = datasetRepository.create(
        data["projectId"],
        data["workflowId"]
    )
    return jsonify(newDataset)

# Delete method, not sure
@datasetRouter.route("/delete/<id>", methods=['DELETE'])
def deleteDataset(id):
    dataset = datasetRepository.delete(id)
    return jsonify(dataset)


@datasetRouter.route("/show/<id>", methods=['GET'])
def showDataset(id):
    dataset = datasetRepository.showById(id)
    return jsonify(dataset)


@datasetRouter.route("/list", methods=['GET'])
def listDatasets():
    datasets = datasetRepository.showAll()
    return jsonify(datasets)
