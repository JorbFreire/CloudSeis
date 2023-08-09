import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .SeismicProjectModel import SeismicProjectModel


class UserModel(database.Model): # type: ignore
	__tablename__ = "users_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)
	email = dbTypes.Column(dbTypes.String)
	password = dbTypes.Column(dbTypes.String)

	seismicProjects: Mapped[List[SeismicProjectModel]] = relationship(SeismicProjectModel)

