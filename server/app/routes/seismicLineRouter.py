from flask import Blueprint, request, jsonify

from ..repositories.SeismicLineRepository import SeismicLineRepository

seismicLineRouter = Blueprint("seismic-line-routes", __name__, url_prefix="/seismic-line")
seismicLineRepository = SeismicLineRepository()

@seismicLineRouter.route("/show/<seismicProjectId>", methods=['GET'])
def showSeismicLine(seismicProjectId):
    seismicLine = seismicLineRepository.showBySeismicProjectId(seismicProjectId)
    return jsonify(seismicLine)

@seismicLineRouter.route("/create", methods=['POST'])
def createSeismicLine():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicLine = seismicLineRepository.create(
        data["seismicProjectId"],
        data["name"]
    )
    return jsonify(newSeismicLine)

@seismicLineRouter.route("/update", methods=['PUT'])
def updateSeismicLine(seismicLineId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicLine = seismicLineRepository.update(
        seismicLineId, data["name"]
    )
    return jsonify({ updatedSeismicLine })

@seismicLineRouter.route("/delete/<id>", methods=['DELETE'])
def deleteSeismicLine(id):
    seismicLine = seismicLineRepository.delete(id)
    return jsonify(seismicLine)

