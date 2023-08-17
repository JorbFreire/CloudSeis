import sqlalchemy as dbTypes

from ..database.connection import database


class SeismicComandModel(database.Model): # type: ignore
	__tablename__ = "seismic_commands_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)
	# stringfied JSON 
	parameters = dbTypes.Column(dbTypes.Text)

	seismicCommandId = dbTypes.Column(dbTypes.ForeignKey( \
		"seismic_workflows_table.id", \
		name="FK_seismic_workflows_table_seismic_commands_table") \
	)

	def getAttributes(self) -> dict[str, str]:
		return {
			"id": self.id,
			"seismicCommandId": self.seismicProjectId,
			"name": self.name,
			"parameters": self.parameters
		}

