import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .ProjectModel import ProjectModel


class UserModel(database.Model):  # type: ignore
    __tablename__ = "users_table"

    id = dbTypes.Column(dbTypes.Uuid, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    email = dbTypes.Column(dbTypes.String, unique=True)
    password = dbTypes.Column(dbTypes.String)
    hashPassword = dbTypes.Column(dbTypes.LargeBinary, unique=True)
    is_admin = dbTypes.Column(dbTypes.Boolean)

    projects: Mapped[
        List[ProjectModel]
    ] = relationship(ProjectModel)

    def getAttributes(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "password": self.password # !Take this OFF!
        }
