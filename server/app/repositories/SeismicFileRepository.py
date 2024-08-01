from os import path, makedirs
import json
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

    def _getSemicUnixCommandString(self, commandsQueue: list, source_file_path: str, target_file_path: str) -> str:
        seismicUnixProcessString = ""
        for orderedCommands in commandsQueue:
            for seismicUnixProgram in orderedCommands.getCommands():
                seismicUnixProcessString += f'{seismicUnixProgram["name"]}'
                seismicUnixProcessString += self._getAllParameters(
                    json.loads((seismicUnixProgram["parameters"]))
                )
                seismicUnixProcessString += f' < {source_file_path} > {target_file_path}'
        return seismicUnixProcessString

    def listByProjectId(self, projectId):
        fileLinks = FileLinkModel.query.filter_by(projectId=projectId).all()

        # *** iterate fileLinks and converte it to list of dicts
        # *** so the api can return this as route response
        fileLinksResponse = list(map(
            lambda link: link.getAttributes(),
            fileLinks
        ))

        return fileLinksResponse

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

        return newFileLink.getAttributes()
        # *** File is blank if marmousi_CS.su is empty

    def update(self, userId, workflowId) -> str:
        workflow = WorkflowModel.query.filter_by(id=workflowId).first()
        workflowParent = WorkflowParentsAssociationModel.query.filter_by(
            workflowId=workflowId
        ).first()

        # datasetAttributes = datasetRepository.create(userId, workflowId)
        fileLink = FileLinkModel.query.filter_by(
            id=workflow.file_link_id
        ).first()

        source_file_path = seismicFilePathRepository.showByWorkflowId(
            workflowId
        )

        target_file_path = seismicFilePathRepository.createByWorkflowId(
            workflowId
        )

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

            # newFileLink = FileLinkModel(
            #     projectId=workflowParent.projectId,
            #     datasetId=datasetAttributes["id"],
            #     data_type="any for now",
            #     name=path.basename(target_file_path)
            # )

            # database.session.add(newFileLink)
            # database.session.commit()

            return str(process_output)
        except Exception as error:
            return str(error)
