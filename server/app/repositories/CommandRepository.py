from ..database.connection import database
from ..models.CommandModel import CommandModel
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..models.WorkflowModel import WorkflowModel
from ..errors.AppError import AppError
from copy import copy


class CommandRepository:
    def show(self, id):
        pass

    def create(self, workflowId, name, parameters):
        workflow = WorkflowModel.query.filter_by(
            id=workflowId
        ).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        orderedCommandsList = OrderedCommandsListModel.query.filter_by(
            workflowId=workflowId
        ).first()

        newCommand = CommandModel(
            name=name,
            parameters=parameters,
            workflowId=workflowId
        )
        database.session.add(newCommand)
        database.session.commit()

        newCommandsList = copy(orderedCommandsList.commandIds)
        newCommandsList.append(newCommand.id)
        orderedCommandsList.commandIds = newCommandsList

        database.session.commit()

        return newCommand.getAttributes()

    def updateParameters(self, id, newParameters):
        command = CommandModel.query.filter_by(id).first()
        if not command:
            raise AppError("Command does not exist", 404)

        command.parameters = newParameters
        database.session.commit()

        return command.getAttributes()

    def delete(self, id):
        pass
