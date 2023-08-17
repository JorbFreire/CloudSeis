import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .SeismicLineModel import SeismicLineModel


class SeismicProjectModel(database.Model): # type: ignore
	__tablename__ = "seismic_projects_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)

	userId = dbTypes.Column( dbTypes.ForeignKey( \
		"users_table.id", \
		name="FK_users_table_seismic_projects_table" \
	))
	seismicLines: Mapped[List[SeismicLineModel]] = relationship(SeismicLineModel)

	def getAttributes(self) -> dict[str, str]:
		return {
			"id": self.id,
			"userId": self.userId,
			"name": self.name,
		}

