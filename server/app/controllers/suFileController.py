from os import path, makedirs
from types import SimpleNamespace
import subprocess

from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel

from ..services.createDataset import createDataset
from ..services.seismicFilePathServices import showWorkflowFilePath, createUploadedFilePath, createDatasetFilePath
from ..services.seismicUnixCommandStringServices import getSemicUnixCommandString

from ..errors.FileError import FileError

def listByProjectId(projectId):
    fileLinks = FileLinkModel.query.filter_by(projectId=projectId).all()

    # *** iterate fileLinks and converte it to list of dicts
    # *** so the api can return this as route response
    fileLinksResponse = list(map(
        lambda link: link.getAttributes(),
        fileLinks
    ))

    return fileLinksResponse


def create(file, projectId) -> str:
    filePath = createUploadedFilePath(
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


def update(userId, workflowId) -> str:
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    workflowParent = WorkflowParentsAssociationModel.query.filter_by(
        workflowId=workflowId
    ).first()

    if not workflow.output_name:
        raise FileError("Output name should be set before running workflow")

    datasetAttributes = createDataset(userId, workflowId)

    source_file_path = showWorkflowFilePath(
        workflowId
    )

    target_file_path = createDatasetFilePath(
        workflowId
    )

    seismicUnixProcessString = getSemicUnixCommandString(
        workflow.orderedCommandsList,
        source_file_path,
        target_file_path
    )

    try:
        process_output = subprocess.check_output(
            seismicUnixProcessString,
            shell=True
        )
        newFileLink = FileLinkModel(
            projectId=workflowParent.getProjectId(),
            datasetId=datasetAttributes["id"],
            data_type="any for now",
            name=path.basename(target_file_path)
        )

        database.session.add(newFileLink)
        database.session.commit()

        return process_output.decode("utf-8")
    except Exception as error:
        return str(error)


suFileController = SimpleNamespace(
    listByProjectId=listByProjectId,
    create=create,
    update=update,
)
