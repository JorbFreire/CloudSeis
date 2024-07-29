from flask import Blueprint, send_file, request, jsonify

from ..errors.AppError import AppError

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.ProjectModel import ProjectModel
from ..models.WorkflowModel import WorkflowModel
from ..repositories.SeismicFileRepository import SeismicFileRepository
from ..repositories.SeismicFilePathRepository import SeismicFilePathRepository

suFileRouter = Blueprint("su-file-routes", __name__, url_prefix="/su-file")
seismicFileRepository = SeismicFileRepository()
seismicFilePathRepository = SeismicFilePathRepository()


@suFileRouter.route("/show/<workflowId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showSuFile(_, workflowId):
    file_path = seismicFilePathRepository.showByWorkflowId(workflowId)
    try:
        return send_file(file_path)  # Faz o download ??
    except Exception as error:
        return str(error)


@suFileRouter.route("/list/<projectId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def listSuFiles(_, projectId):
    fileLinksList = seismicFileRepository.listByProjectId(projectId)
    return jsonify(fileLinksList)


@suFileRouter.route("/create/<projectId>", methods=['POST'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createSuFile(_, projectId):
    file = request.files['file']
    if 'file' not in request.files:
        raise AppError("No file part in the request")

    fileLink = seismicFileRepository.create(file, projectId)
    return {"fileLink": fileLink}


@suFileRouter.route("/update/<workflowId>", methods=['PUT'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateSuFile(userId, workflowId):
    process_output = seismicFileRepository.update(userId, workflowId)
    return jsonify({
        "process_output": process_output
    })
