import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship

from ..database.connection import database
from .SeismicWorkflowModel import SeismicWorkflowModel


class SeismicLineModel(database.Model): # type: ignore
	__tablename__ = "seismic_lines_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)

	seismicLineIds = dbTypes.ForeignKey("seismic_workflows_table.id")
	seismicLines = relationship(SeismicWorkflowModel)

