import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .CommandModel import CommandModel
from .OrderedCommandsListModel import OrderedCommandsListModel


class WorkflowModel(database.Model):  # type: ignore
    __tablename__ = "workflows_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    file_name = dbTypes.Column(dbTypes.String)

    commands: Mapped[
        List[CommandModel]
    ] = relationship(CommandModel)

    orderedCommandsList: Mapped[
        List[CommandModel]
    ] = relationship(OrderedCommandsListModel)

    def getResumedAttributes(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

    def getAttributes(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "file_name": self.file_name,
            "commands": self.orderedCommandsList[0].getCommands(),
        }
