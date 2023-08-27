from ..database.connection import database
from ..models.CommandModel import CommandModel
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..models.WorkflowModel import WorkflowModel
from ..errors.AppError import AppError
from copy import copy


class CommandRepository:
    def show(self, id):
        pass

    def create(self, workflowId):
        workflow = WorkflowModel.query.filter_by(
            id=workflowId
        ).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        orderedCommandsList = OrderedCommandsListModel.query.filter_by(
            workflowId=workflowId
        ).first()

        newCommand = CommandModel(
            name="new command",
            parameters="parameters",
            workflowId=workflowId
        )
        database.session.add(newCommand)
        database.session.commit()

        print('orderedCommandsList["commandIds"]')
        print(orderedCommandsList.commandIds)
        newCommandsList = copy(orderedCommandsList.commandIds)
        newCommandsList.append(newCommand.id)
        orderedCommandsList.commandIds = newCommandsList
        database.session.commit()

        return newCommand.getAttributes()

    def update(self, id, newCommandData):
        pass

    def delete(self, id):
        pass
