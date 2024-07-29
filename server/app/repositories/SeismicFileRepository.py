from json import loads
from os import path, makedirs
import subprocess


from .SeismicFilePathRepository import SeismicFilePathRepository
from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..repositories.DatasetRepository import DatasetRepository

seismicFilePathRepository = SeismicFilePathRepository()
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
        filePath = seismicFilePathRepository.createByProjectId(
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

    def update(self, userId, workflowId) -> str: 
        # Must create file at target_file_path
        # Must get the file from the workflow
        # Then save it into target_file_path

        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        workflowParent = WorkflowParentsAssociationModel.query.filter_by(workflowId=workflowId).first()

        datasetAttributes = datasetRepository.create(userId, workflowId)

        source_file_path = seismicFilePathRepository.showByWorkflowId(workflowId)
        source_file_path += workflow.file_name

        target_file_path = seismicFilePathRepository.createByWorkflowId(workflowId)

        seismicUnixProcessString = self._getSemicUnixCommandString(
            workflow.orderedCommandsList,
            source_file_path,
            target_file_path
        )


        newFileLink = FileLinkModel(
            projectId=workflowParent.projectId,
            datasetId=datasetAttributes["id"],
            data_type="any for now",
            name=path.basename(target_file_path)
        )
        database.session.add(newFileLink) # Must create everytime or just in success process? 
        database.session.commit()

        try:
            process_output = subprocess.check_output(
                seismicUnixProcessString,
                shell=True
            )
            return str(process_output)
        except Exception as error:
            return str(error)
