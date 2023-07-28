import sqlalchemy as dbTypes

from ..database.connection import database


class SeismicComandModel(database.Model): # type: ignore
	__tablename__ = "seismic_commands_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)

	# stringfied JSON 
	parameters = dbTypes.Column(dbTypes.Text)

