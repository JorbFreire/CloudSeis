import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .LineModel import LineModel


class ProjectModel(database.Model):  # type: ignore
    __tablename__ = "projects_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)

    userId = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.id",
        name="FK_users_table_projects_table"
    ))
    lines: Mapped[
        List[LineModel]
    ] = relationship(LineModel)

    def getAttributes(self) -> dict[str, str]:
        return {
            "id": self.id,
            "userId": self.userId,
            "name": self.name,
        }
