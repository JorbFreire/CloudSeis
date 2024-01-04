import sqlalchemy as dbTypes

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
    datasetId = dbTypes.Column(dbTypes.ForeignKey(
        "datasets_table.id",
        name="FK_workflow_parents_association_table_dataset_table"
    ))
    # Feature de ser filho ou de project ou de line
    lineId = dbTypes.Column(dbTypes.ForeignKey(
        "lines_table.id",
        name="FK_workflow_parents_association_table_lines_table"
    ))
    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_workflow_parents_association_table_projects_table"
    ))
    
    def getAttributes(self):
        return {
            "projectId": self.projectId,
            "lineId": self.lineId,
            "workflowId": self.workflowId,
        }
