from flask import Blueprint, request, jsonify

from ..repositories.SeismicProjectRepository import SeismicProjectRepository

seismicProjectRouter = Blueprint("seismic-project-routes", __name__, url_prefix="/seismic-project")
seismicProjectRepository = SeismicProjectRepository()

@seismicProjectRouter.route("/show", methods=['GET'])
def showSeismicProject(seismicProjectId):
    seismicProject = seismicProjectRepository.show(seismicProjectId)
    return jsonify({ seismicProject })

@seismicProjectRouter.route("/create", methods=['POST'])
def createSeismicProject():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicProject = seismicProjectRepository.create(data.seismicProject)
    return jsonify({ newSeismicProject })

@seismicProjectRouter.route("/update", methods=['PUT'])
def updateSeismicProject(seismicProjectId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicProject = seismicProjectRepository.update(seismicProjectId, data.seismicProject)
    return jsonify({ updatedSeismicProject })

@seismicProjectRouter.route("/delete", methods=['DELETE'])
def deleteSeismicProject(seismicProjectId):
    seismicProject = seismicProjectRepository.delete(seismicProjectId)
    return jsonify({ seismicProject })

