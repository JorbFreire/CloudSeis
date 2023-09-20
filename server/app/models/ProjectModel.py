import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .LineModel import LineModel
from .WorkflowModel import WorkflowModel


class ProjectModel(database.Model):  # type: ignore
    __tablename__ = "projects_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)

    userId = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.id",
        name="FK_users_table_projects_table"
    ))

    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(secondary=WorkflowParentsAssociationModel)

    lines: Mapped[
        List[LineModel]
    ] = relationship(LineModel)


    def getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) is 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.projectId.in_(
                [association.workflowId for association in self.workflowParentAssociations]
            )
        ).all()
        return [workflow.getResumedAttributes() for workflow in workflows]

    def getAttributes(self) -> dict[str, str]:
        return {
            "id": self.id,
            "userId": self.userId,
            "name": self.name,
        }
