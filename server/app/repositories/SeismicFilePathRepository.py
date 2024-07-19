from os import getcwd, path, makedirs
from datetime import datetime
from uuid import UUID

from ..models.WorkflowModel import WorkflowModel
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel


class SeismicFilePathRepository:
    def _getRandomString():
        return datetime.now().strftime("%d%m%Y_%H%M%S")

    def _getSuFilePath(self, unique_filename, user_email, projectId):
        file_path = f'{getcwd()}/static/{user_email}/{projectId}/{unique_filename}'
        return file_path

    def showByWorkflowId(self, workflowId) -> str:
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()

        unique_filename = workflow.file_name.replace(".su", "_")
        unique_filename = unique_filename.replace(" ", "_")
        unique_filename = f'{unique_filename}{self._getRandomString()}.su'

        file_path = self._getSuFilePath(
            workflow.file_name,
            workflow.owner_email,
            workflow.getProjectId()
        )
        return file_path

    # *** Expected to be used when uploading a new file
    def createByProjectId(self, input_file_name, projectId):
        project = ProjectModel.query.filter(id=projectId).first
        user = UserModel.query.filter_by(id=UUID(project.userId)).first()

        filePath = self._getSuFilePath(
            input_file_name,
            user.email,
            projectId
        )

        return filePath

    # *** Expected to be used when updating a file and generating a dataset
    def createByWorkflowId(self, workflowId):
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()

        source_file_path = self.showByWorkflowId(workflowId)
        directory = path.dirname(source_file_path)
        target_file_path = f'{workflow.file_name.replace(".su", "_")}{self._getRandomString()}.su'

        target_file_path = path.join(
            directory,
            "datasets",
            workflowId,
            target_file_path
        )
        datasetsDirectory = path.dirname(target_file_path)
        if not path.exists(datasetsDirectory):
            makedirs(datasetsDirectory)
        pass
