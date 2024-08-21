from uuid import UUID

from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from ..models.CommandModel import CommandModel

from ..repositories.WorkflowRepository import workflowRepository
from ..repositories.CommandRepository import commandRepository
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository


def createDataset(userId, baseWorkflowId) -> dict:
    # *** this method duplicate a workflow and keep it as history
    # *** being chidren of the dataset table.
    # *** Keeping the generated file and the workflow used to get it
    user = UserModel.query.filter_by(id=UUID(userId)).first()

    baseWorkflow = WorkflowModel.query.filter_by(
        id=baseWorkflowId
    ).first()

    commands = CommandModel.query.filter_by(
        workflowId=baseWorkflowId
    ).all()

    dataset = DataSetModel(
        workflowId=baseWorkflowId,
        owner_email=user.email
    )
    database.session.add(dataset)
    database.session.commit()

    newWorkflowData = {
        "name": f"{baseWorkflow.name} - dataset",
        "parentType": "datasetId",
    }

    newWorkflow = workflowRepository.create(
        userId,
        newWorkflowData,
        dataset.id,
    )

    orderedCommandsListRepository.create(newWorkflow.id)

    workflowRepository.updateFilePath(
        newWorkflow.id,
        baseWorkflow.file_link_id
    )

    for command in commands:
        commandRepository.create(
            userId,
            newWorkflow.id,
            command.name,
            command.parameters
        )
        database.session.add(command)

    database.session.commit()

    return dataset.getAttributes()
