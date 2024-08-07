from os import getcwd, path, makedirs
from datetime import datetime

from ..models.WorkflowModel import WorkflowModel
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel


# todo: turn into services and call in controller
class SeismicFilePathRepository:
    def _getUniqueString(self) -> str:
        return datetime.now().strftime("%d%m%Y_%H%M%S")

    def _getSuFilePath(self, unique_filename, user_email, projectId) -> str:
        file_path = f'{getcwd()}/static/{user_email}/{projectId}/{unique_filename}'
        return file_path

    def showByWorkflowId(self, workflowId) -> str:
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()

        file_path = self._getSuFilePath(
            workflow.getSelectedFileName(),
            workflow.owner_email,
            workflow.workflowParent[0].getProjectId()
        )
        return file_path

    # *** Expected to be used when uploading a new file
    def createByProjectId(self, input_file_name, projectId) -> str:
        project = ProjectModel.query.filter_by(id=projectId).first()
        user = UserModel.query.filter_by(id=str(project.userId)).first()

        filePath = self._getSuFilePath(
            input_file_name,
            user.email,
            projectId
        )

        return filePath

    # *** Expected to be used when updating a file and generating a dataset
    def createByWorkflowId(self, workflowId) -> str:
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()

        source_file_path = self.showByWorkflowId(workflowId)
        directory = path.dirname(source_file_path)
        target_file_path = f'{workflow.getSelectedFileName().replace(".su", "_")}{self._getUniqueString()}.su'

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
