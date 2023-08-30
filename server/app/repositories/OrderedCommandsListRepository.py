from ..database.connection import database
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..errors.AppError import AppError


class OrderedCommandsListRepository:
    def create(self, workflowId):
        orderedCommandsList = OrderedCommandsListModel(
            workflowId=workflowId,
            commandIds=[],
        )
        database.session.add(orderedCommandsList)
        database.session.commit()

    def update(self, id, newOrder):
        orderedCommandsList = OrderedCommandsListModel.query.filter_by(
            id
        ).first()
        if not orderedCommandsList:
            raise AppError("OrderedComandsList does not exist")

        orderedCommandsList.commandIds = newOrder
        database.session.commit()

        return orderedCommandsList.getAttributes()
