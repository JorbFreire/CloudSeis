from uuid import UUID
from ..models.UserModel import UserModel
from ..database.connection import database
from ..models.CommandModel import CommandModel
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..models.WorkflowModel import WorkflowModel
from ..errors.AppError import AppError
from copy import copy
from json import dumps


class CommandRepository:
    def show(self, id):
        command = CommandModel.query.filter_by(id=id).first()
        return command.getAttributes()

    def create(self, userId, workflowId, name, parameters):
        user = UserModel.query.filter_by(id=UUID(userId)).first()
        if not user:
            raise AppError("User does not exist", 404)

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
            workflowId=workflowId,
            owner_email=user.email
        )
        database.session.add(newCommand)
        database.session.commit()

        newCommandsList = copy(orderedCommandsList.commandIds)
        newCommandsList.append(newCommand.id)
        orderedCommandsList.commandIds = newCommandsList

        database.session.commit()

        return newCommand.getAttributes()

    def updateParameters(self, id, newParameters):
        if isinstance(newParameters, dict):
            newParameters = dumps(newParameters)
        command = CommandModel.query.filter_by(id=id).first()
        if not command:
            raise AppError("Command does not exist", 404)

        command.parameters = newParameters
        database.session.commit()

        return command.getAttributes()

    def delete(self, id):
        command = CommandModel.query.filter_by(id=id).first()
        if not command:
            raise AppError("Command does not exist", 404)

        database.session.delete(command)
        database.session.commit()

        return command.getAttributes()
