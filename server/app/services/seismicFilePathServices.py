from os import getcwd, path, makedirs

from ..models.WorkflowModel import WorkflowModel
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel
from ..models.DataSetModel import DataSetModel


def _generateSuFilePath(unique_filename, user_email, projectId) -> str:
    file_path = f'{getcwd()}/static/{user_email}/{projectId}/{unique_filename}'
    return file_path


def _buildFilePath(folderBaseWorkflowId, output_name):
    source_file_path = showWorkflowFilePath(folderBaseWorkflowId)
    directory = path.dirname(source_file_path)
    target_file_name = f'{output_name}.su'

    target_file_path = path.join(
        directory,
        "datasets",
        f"from_workflow_{folderBaseWorkflowId}",
        target_file_name
    )

    return target_file_path


def showWorkflowFilePath(workflowId) -> str:
    # *** Show the file path for the input file of a given workflow
    # *** Can be the workflow maded to keep dataset history
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()

    file_path = _generateSuFilePath(
        workflow.getSelectedFileName(),
        workflow.owner_email,
        workflow.workflowParent.getProjectId()
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

    # *** get origin workflow
    target_file_path = _buildFilePath(workflowId, f'{workflow.output_name}.su')

    datasetsDirectory = path.dirname(target_file_path)
    if not path.exists(datasetsDirectory):
        makedirs(datasetsDirectory)

    return target_file_path


def showDatasetFilePath(workflowId):
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    datasetId = workflow.workflowParent.datasetId

    dataset = DataSetModel.query.filter_by(id=datasetId).first()

    # *** origin workflow
    target_file_path = _buildFilePath(dataset.workflowId, workflow.output_name)

    print(target_file_path)

    return target_file_path
