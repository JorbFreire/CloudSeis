import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowModel import WorkflowModel


class LineModel(database.Model):  # type: ignore
    __tablename__ = "lines_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_projects_table_lines_table"
    ))
    workflows: Mapped[
        List[WorkflowModel]
    ] = relationship(WorkflowModel)

    def getAttributes(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            "id": self.id,
            "projectId": self.projectId,
            "name": self.name,
            "workflows": [workflow.getResumedAttributes() for workflow in self.workflows],
        }
