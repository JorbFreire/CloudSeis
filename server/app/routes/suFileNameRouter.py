from flask import Blueprint, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.WorkflowModel import WorkflowModel

from ..services.seismicFilePathServices import showWorkflowFilePath, showDatasetFilePath

suFileNameRouter = Blueprint(
    "su-file-name-routes",
    __name__,
    url_prefix="/su-file-path"
)


@suFileNameRouter.route("/show-path/<workflowId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showSuFilePath(_, workflowId):
    # *** no controller layer for this route, no adcional rules *** #
    file_path = showWorkflowFilePath(workflowId)
    return jsonify({
        "file_path": file_path
    })


@suFileNameRouter.route("/dataset/show-path/<workflowId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showDatasetSuFilePath(_, workflowId):
    # *** no controller layer for this route, no adcional rules *** #
    file_path = showDatasetFilePath(workflowId)
    return jsonify({
        "file_path": file_path,
    })
