import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .WorkflowModel import WorkflowModel


class DataSetModel(database.Model):
    __tablename__ = "datasets_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_dataset_table"
    ))

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_projects_datasets"
    ))

    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(WorkflowParentsAssociationModel)


    def _getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) == 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.id.in_(
                [association.workflowId for association in self.workflowParentAssociations]
            )
        ).all()
        return [workflow.getAttributes() for workflow in workflows]

    def getAttributes(self) -> dict:
        return {
            "id": self.id,
            "workflows": self._getWorkflows()
        }
