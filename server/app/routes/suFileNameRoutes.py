from flask import Blueprint, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.WorkflowModel import WorkflowModel

from ..repositories.SeismicFilePathRepository import SeismicFilePathRepository

suFileNameRouter = Blueprint(
    "su-file-name-routes",
    __name__,
    url_prefix="/su-file-path"
)

seismicFilePathRepository = SeismicFilePathRepository()


@suFileNameRouter.route("/show-path/<workflowId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showSuFilePath(_, workflowId):
    file_path = seismicFilePathRepository.showByWorkflowId(workflowId)
    return jsonify({
        "file_path": file_path
    })
