from flask import Blueprint, request, jsonify

from ..repositories.SeismicWorkflowRepository import SeismicWorkflowRepository

seismicWorkflowRouter = Blueprint("seismic-workflow-routes", __name__, url_prefix="/seismic-workflow")
seismicWorkflowRepository = SeismicWorkflowRepository()

@seismicWorkflowRouter.route("/show/<id>", methods=['GET'])
def showSeismicWorkflow(id):
    seismicWorkflow = seismicWorkflowRepository.showById(id)
    return jsonify(seismicWorkflow)

@seismicWorkflowRouter.route("/create", methods=['POST'])
def createSeismicWorkflow():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicWorkflow = seismicWorkflowRepository.create(
        data["lineId"],
        data["name"]
    )
    return jsonify(newSeismicWorkflow)

@seismicWorkflowRouter.route("/update/<id>", methods=['PUT'])
def updateSeismicWorkflow(id):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    updatedSeismicWorkflow = seismicWorkflowRepository.updateName(
        id,
        data["name"]
    )
    return jsonify(updatedSeismicWorkflow)

@seismicWorkflowRouter.route("/delete/<id>", methods=['DELETE'])
def deleteSeismicWorkflow(id):
    seismicWorkflow = seismicWorkflowRepository.delete(id)
    return jsonify(seismicWorkflow)

