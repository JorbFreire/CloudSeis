import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .ProjectModel import ProjectModel


class UserModel(database.Model):  # type: ignore
    __tablename__ = "users_table"

    id = dbTypes.Column(dbTypes.Uuid, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    email = dbTypes.Column(dbTypes.String)
    password = dbTypes.Column(dbTypes.String)

    projects: Mapped[
        List[ProjectModel]
    ] = relationship(ProjectModel)

    def getAttributes(self) -> dict[str, str]:
        return {"id": self.id, "name": self.name, "email": self.email}
