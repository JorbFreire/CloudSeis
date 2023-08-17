from flask import Blueprint, request, jsonify

from ..repositories.SeismicProjectRepository import SeismicProjectRepository

seismicProjectRouter = Blueprint("seismic-project-routes", __name__, url_prefix="/seismic-project")
seismicProjectRepository = SeismicProjectRepository()

@seismicProjectRouter.route("/list/<userId>", methods=['GET'])
def showSeismicProject(userId):
    seismicProject = seismicProjectRepository.showByUserId(userId)
    return jsonify(seismicProject)

@seismicProjectRouter.route("/create", methods=['POST'])
def createSeismicProject():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newSeismicProject = seismicProjectRepository.create(data["userId"], data["name"])
    return jsonify(newSeismicProject)

@seismicProjectRouter.route("/update/<seismicProjectId>", methods=['PUT'])
def updateSeismicProject(seismicProjectId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedSeismicProject = seismicProjectRepository.updateName(seismicProjectId, data["name"])
    return jsonify(updatedSeismicProject)

@seismicProjectRouter.route("/delete/<seismicProjectId>", methods=['DELETE'])
def deleteSeismicProject(seismicProjectId):
    seismicProject = seismicProjectRepository.delete(seismicProjectId)
    return jsonify(seismicProject)

