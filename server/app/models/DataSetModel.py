import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .OrderedCommandsListModel import OrderedCommandsListModel
from .WorkflowModel import WorkflowModel
from .CommandModel import CommandModel 


class DataSetModel(database.Model):
    __tablename__ = "datasets_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "datasets_table.id",
        name="FK_projects_datasets"
    ))

    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(WorkflowParentsAssociationModel)

    orderedCommands: Mapped[
        List[OrderedCommandsListModel]
    ] = relationship(OrderedCommandsListModel)

    def _getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) == 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.id.in_(
                [association.workflowId for association in self.workflowParentAssociations]
            )
        ).all()
        return [workflow.getResumedAttributes() for workflow in workflows]

    def _getCommands(self):
        commands = CommandModel.query.filter(
            CommandModel.id._in(
                [command.workflowId for command in self.orderedCommands]
            )
        )
        return [command.getAttributes() for command in commands]

    def getAttributes(self) -> dict:
        return {
            "id": self.id,
            "workflows": self._getWorkflows(),
            "commands": self._getCommands()
        }
