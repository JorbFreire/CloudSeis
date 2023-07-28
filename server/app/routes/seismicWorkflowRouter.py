from flask import Blueprint, request, jsonify

from ..repositories.SeismicWorkflowRepository import SeismicWorkflowRepository

seismicWorkflowRouter = Blueprint("seismic-workflow-routes", __name__, url_prefix="/seismicWorkflow")
seismicWorkflowRepository = SeismicWorkflowRepository()

@seismicWorkflowRouter.route("/show", methods=['GET'])
def showSeismicWorkflow(seismicWorkflowId):
    seismicWorkflow = seismicWorkflowRepository.show(seismicWorkflowId)
    return jsonify({ seismicWorkflow })

@seismicWorkflowRouter.route("/create", methods=['POST'])
def createSeismicWorkflow():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicWorkflow = seismicWorkflowRepository.create(data.seismicWorkflow)
    return jsonify({ newSeismicWorkflow })

@seismicWorkflowRouter.route("/update", methods=['PUT'])
def updateSeismicWorkflow(seismicWorkflowId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicWorkflow = seismicWorkflowRepository.update(seismicWorkflowId, data.seismicWorkflow)
    return jsonify({ updatedSeismicWorkflow })

@seismicWorkflowRouter.route("/delete", methods=['DELETE'])
def deleteSeismicWorkflow(seismicWorkflowId):
    seismicWorkflow = seismicWorkflowRepository.delete(seismicWorkflowId)
    return jsonify({ seismicWorkflow })

