import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship

from ..database.connection import database
from .SeismicLineModel import SeismicLineModel


class SeismicProjectModel(database.Model): # type: ignore
	__tablename__ = "seismic_projects_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)

	seismicLineIds = dbTypes.ForeignKey("seismic_lines_table.id")
	seismicLines = relationship(SeismicLineModel)

