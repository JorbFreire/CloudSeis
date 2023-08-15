import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .SeismicComandModel import SeismicComandModel


class SeismicWorkflowModel(database.Model): # type: ignore
	__tablename__ = "seismic_workflows_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)
	seismic_file_name = dbTypes.Column(dbTypes.String)

	seismicLineId = dbTypes.Column( dbTypes.ForeignKey( \
		"seismic_lines_table.id", \
		name="FK_seismic_lines_table_seismic_workflows_table" \
	))
	seismicCommands: Mapped[List[SeismicComandModel]] = relationship(SeismicComandModel)

	def getResumedAttributes(self) -> dict[str, str | list[dict[str, str]]]:
		return {
			"id": self.id,
			"name": self.name,
		}

	def getAttributes(self) -> dict[str, str | list[dict[str, str]]]:
		return {
			"id": self.id,
			"seismicLineId": self.seismicLineId,
			"name": self.name,
			"seismic_file_name": self.seismic_file_name,
			"seismicCommands": [command.getAttributes() for command in self.seismicCommands],
		}

