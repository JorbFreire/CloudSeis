from os import getcwd, path, makedirs
from datetime import datetime

from ..models.WorkflowModel import WorkflowModel
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel


# todo: turn into services and call in controller
def _generateUniqueString() -> str:
    return datetime.now().strftime("%d%m%Y_%H%M%S")


def _generateSuFilePath(unique_filename, user_email, projectId) -> str:
    file_path = f'{getcwd()}/static/{user_email}/{projectId}/{unique_filename}'
    return file_path


def showWorkflowFilePath(workflowId) -> str:
    # *** Show the file path for the input file of a given workflow
    # *** Can be the workflow maded to keep dataset history
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()

    file_path = _generateSuFilePath(
        workflow.getSelectedFileName(),
        workflow.owner_email,
        workflow.workflowParent[0].getProjectId()
    )
    return file_path


def createUploadedFilePath(input_file_name, projectId) -> str:
    # *** Expected to be used when uploading a new file
    project = ProjectModel.query.filter_by(id=projectId).first()
    user = UserModel.query.filter_by(id=str(project.userId)).first()

    filePath = _generateSuFilePath(
        input_file_name,
        user.email,
        projectId
    )

    return filePath


def createDatasetFilePath(workflowId) -> str:
    # *** Expected to be used when updating a file and generating a dataset
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()

    source_file_path = showWorkflowFilePath(workflowId)
    directory = path.dirname(source_file_path)
    target_file_path = f'{workflow.getSelectedFileName().replace(".su", "_")}{_generateUniqueString()}.su'

    target_file_path = path.join(
        directory,
        "datasets",
        f"from_workflow_{workflowId}",
        target_file_path
    )
    datasetsDirectory = path.dirname(target_file_path)
    if not path.exists(datasetsDirectory):
        makedirs(datasetsDirectory)

    return target_file_path
