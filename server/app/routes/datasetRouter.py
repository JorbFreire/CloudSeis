from flask import Blueprint, request, jsonify

from ..repositories.DatasetRepository import DatasetRepository

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")
datasetRepository = DatasetRepository()

@datasetRouter.route("/create", methods=['POST'])
def createDataset():
    data = request.get_json()
    if data is None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    newDataset = datasetRepository.create(data["projectId"], data["workflowId"])
    return jsonify(newDataset)

@datasetRouter.route("/show/<id>", methods=['GET'])
def showDataset(id):
    dataset = datasetRepository.showById(id)
    return jsonify(dataset)

@datasetRouter.route("/list", methods=['GET'])
def listDatasets():
    datasets = datasetRepository.showAll()
    return jsonify(datasets)
