import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .WorkflowModel import WorkflowModel
# Projeto
    # Dataset

        # .su2
  # Workflow djdj
    # Workflow2

class DataSet(database.Model):
    __tablename__ = "datasets_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    currentSate = dbTypes.Column(dbTypes.String)

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "datasets_table.id",
        name="FK_projects_datasets"
    ))

    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(WorkflowParentsAssociationModel)

    def _getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) == 0:
            return []
        workflows = WorkflowModel.query.filter().all()
        return [workflow.getResumedAttributes() for workflow in workflows]

    def getAttributes(self) -> dict:
        return {
            "id": self.id,
            "workflows": self._getWorkflows(),
            "currentSate": self.currentSate
        }

