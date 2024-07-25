from json import loads
from os import path, makedirs
import subprocess

from .SeismicFilePathRepository import SeismicFilePathRepository

from ..database.connection import database

from ..models.UserModel import UserModel
from ..models.FileLinkModel import FileLinkModel
from ..models.WorkflowModel import WorkflowModel

from ..repositories.DatasetRepository import DatasetRepository

seismicFileRepository = SeismicFilePathRepository()
datasetRepository = DatasetRepository()


class SeismicFileRepository:
    def _getParameter(self, parameterValues: list | str | float | int | bool) -> str:
        parameterValuesProcessString = ""
        if not isinstance(parameterValues, list):
            parameterValuesProcessString += f'{parameterValues}'
            return parameterValuesProcessString

        for index, parameterValue in enumerate(parameterValues):
            if index < len(parameterValues) - 1:
                parameterValuesProcessString += f'{parameterValue},'
                continue
            parameterValuesProcessString += f'{parameterValue}'

        return parameterValuesProcessString

    def _getAllParameters(self, parameters) -> str:
        parametersProcessString = ""
        for parameterKey, parameterValues in parameters.items():
            if not parameterValues:
                continue
            parametersProcessString += f' {parameterKey}='
            parametersProcessString += self._getParameter(parameterValues)
        return parametersProcessString

    def _getSemicUnixCommandString(self, commandsQueue: list, source_file_path: str, changed_file_path: str) -> str:
        seismicUnixProcessString = ""
        for orderedCommands in commandsQueue:
            for seismicUnixProgram in orderedCommands.getCommands():
                seismicUnixProcessString += f'{seismicUnixProgram["name"]}'
                seismicUnixProcessString += self._getAllParameters(
                    loads((seismicUnixProgram["parameters"]))
                )
                seismicUnixProcessString += f' < {source_file_path} > {changed_file_path}'
        return seismicUnixProcessString

    def listByProjectId(self, projectId):
        fileLinks = FileLinkModel.query.filter_by(projectId=projectId).all()
        return fileLinks

    def create(self, file, projectId) -> str:
        filePath = seismicFileRepository.createByProjectId(
            file.filename,
            projectId
        )

        newFileLink = FileLinkModel(
            projectId=projectId,
            data_type="any for now",
            name=path.basename(filePath)
        )
        database.session.add(newFileLink)
        database.session.commit()

        directory = path.dirname(filePath)
        if not path.exists(directory):
            makedirs(directory)
        file.save(filePath)
        return filePath
        # *** File is blank if marmousi_CS.su is empty

    def update(self, workflowId) -> str:
        user = UserModel.query.filter_by(email=workflow.owner_email).first()
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()

        datasetRepository.create(str(user.id), workflow.id)

        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        source_file_path = seismicFileRepository.showByWorkflowId(workflowId)
        target_file_path = seismicFileRepository.createByWorkflowId(workflowId)

        seismicUnixProcessString = self._getSemicUnixCommandString(
            workflow.orderedCommandsList,
            source_file_path,
            target_file_path
        )

        try:
            process_output = subprocess.check_output(
                seismicUnixProcessString,
                shell=True
            )

            return str(process_output)
        except Exception as error:
            return str(error)
