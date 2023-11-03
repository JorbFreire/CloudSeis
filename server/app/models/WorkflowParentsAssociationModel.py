import sqlalchemy as dbTypes
from typing import List

from ..database.connection import database
from .WorkflowModel import WorkflowModel


class WorkflowParentsAssociationModel(database.Model):  # type: ignore
    __tablename__ = "workflow_parents_association_table"

    workflowId = dbTypes.Column(
        dbTypes.ForeignKey(
            "workflows_table.id",
            name="FK_workflow_parents_association_table_workflows_table"
        ),
        primary_key=True
    )
    lineId = dbTypes.Column(dbTypes.ForeignKey(
        "lines_table.id",
        name="FK_workflow_parents_association_table_lines_table"
    ))
    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_workflow_parents_association_table_projects_table"
    ))

    def getAttributes(self) -> dict[str, str]:
        return {
            "projectId": self.projectId,
            "lineId": self.lineId,
            "workflowId": self.workflowId,
        }
