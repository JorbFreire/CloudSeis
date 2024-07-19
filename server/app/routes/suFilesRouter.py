from flask import Blueprint, send_file, request, jsonify

from ..errors.AppError import AppError

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.ProjectModel import ProjectModel
from ..repositories.SeismicFileRepository import SeismicFileRepository

suFileRouter = Blueprint("su-file-routes", __name__, url_prefix="/su-file")
seismicFileRepository = SeismicFileRepository()

# ? note sure if this "/ should be keep or not"
@suFileRouter.route("/", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su') # Faz o download ??
    except Exception as error:
        return str(error)


# ? note sure if this "/ should be keep or not"
@suFileRouter.route("/create/<projectId>", methods=['POST'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createSuFile(userId, *_, **kwargs):
    file = request.files['file']
    if 'file' not in request.files:
        raise AppError("No file part in the request")

    projectId = int(list(kwargs.values())[0])
    unique_filename = seismicFileRepository.create(file, userId, projectId)
    return {"unique_filename": unique_filename}


# Understans <unique_filename> -> What it is, which file is and why it is necessary
@suFileRouter.route("/<unique_filename>/<workflowId>", methods=['PUT'])
# @decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateSuFile(unique_filename, workflowId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )

    # seismicUnixCommandsQueue = data["seismicUnixCommandsQueue"]
    process_output = seismicFileRepository.update(unique_filename, workflowId)
    return jsonify({
        "process_output": process_output
    })
