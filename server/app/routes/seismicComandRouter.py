from flask import Blueprint, request, jsonify

from ..repositories.SeismicComandRepository import SeismicComandRepository

seismicComandRouter = Blueprint("seismic-comand-routes", __name__, url_prefix="/seismicComand")
seismicComandRepository = SeismicComandRepository()

@seismicComandRouter.route("/show", methods=['GET'])
def showSeismicComand(seismicComandId):
    seismicComand = seismicComandRepository.show(seismicComandId)
    return jsonify({ seismicComand })

@seismicComandRouter.route("/create", methods=['POST'])
def createSeismicComand():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicComand = seismicComandRepository.create(data.seismicComand)
    return jsonify({ newSeismicComand })

@seismicComandRouter.route("/update", methods=['PUT'])
def updateSeismicComand(seismicComandId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicComand = seismicComandRepository.update(seismicComandId, data.seismicComand)
    return jsonify({ updatedSeismicComand })

@seismicComandRouter.route("/delete", methods=['DELETE'])
def deleteSeismicComand(seismicComandId):
    seismicComand = seismicComandRepository.delete(seismicComandId)
    return jsonify({ seismicComand })

