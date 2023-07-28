import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship

from ..database.connection import database
from .SeismicComandModel import SeismicComandModel


class SeismicWorkflowModel(database.Model): # type: ignore
	__tablename__ = "seismic_workflows_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)
	seismic_file_name = dbTypes.Column(dbTypes.String)

	seismicLineIds = dbTypes.ForeignKey("seismic_commands_table.id")
	seismicLines = relationship(SeismicComandModel)

