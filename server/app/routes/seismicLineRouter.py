from flask import Blueprint, request, jsonify

from ..repositories.SeismicLineRepository import SeismicLineRepository

seismicLineRouter = Blueprint("seismic-line-routes", __name__, url_prefix="/seismicLine")
seismicLineRepository = SeismicLineRepository()

@seismicLineRouter.route("/show", methods=['GET'])
def showSeismicLine(seismicLineId):
    seismicLine = seismicLineRepository.show(seismicLineId)
    return jsonify({ seismicLine })

@seismicLineRouter.route("/create", methods=['POST'])
def createSeismicLine():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicLine = seismicLineRepository.create(data.seismicLine)
    return jsonify({ newSeismicLine })

@seismicLineRouter.route("/update", methods=['PUT'])
def updateSeismicLine(seismicLineId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicLine = seismicLineRepository.update(seismicLineId, data.seismicLine)
    return jsonify({ updatedSeismicLine })

@seismicLineRouter.route("/delete", methods=['DELETE'])
def deleteSeismicLine(seismicLineId):
    seismicLine = seismicLineRepository.delete(seismicLineId)
    return jsonify({ seismicLine })

