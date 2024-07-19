import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .CommandModel import CommandModel
from .OrderedCommandsListModel import OrderedCommandsListModel
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel


class WorkflowModel(database.Model):  # type: ignore
    __tablename__ = "workflows_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    # todo: file_name shall be moved to the project and make a selectable here
    file_name = dbTypes.Column(dbTypes.String)

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_workflows_table"
    ))

    commands: Mapped[
        List[CommandModel]
    ] = relationship(CommandModel, cascade='all, delete-orphan')

    orderedCommandsList: Mapped[
        List[CommandModel]
    ] = relationship(OrderedCommandsListModel)

    workflowParent: Mapped[
        WorkflowParentsAssociationModel
    ] = relationship(WorkflowParentsAssociationModel, cascade="all, delete-orphan")

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
