import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship

from ..database.connection import database
from .SeismicProjectModel import SeismicProjectModel


class UserModel(database.Model): # type: ignore
	__tablename__ = "users_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)
	email = dbTypes.Column(dbTypes.String)
	password = dbTypes.Column(dbTypes.String)

	seismicProjectIds = dbTypes.ForeignKey("seismic_projects_table.id")
	seismicProjects = relationship(SeismicProjectModel)

