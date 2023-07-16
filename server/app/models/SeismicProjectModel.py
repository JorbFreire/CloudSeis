import sqlalchemy as dbTypes

from ..database.connection import database


class SeismicProjectModel(database.Model): # type: ignore
	__tablename__ = "seismic_project_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	title = dbTypes.Column(dbTypes.String)
	seismic_file_name = dbTypes.Column(dbTypes.String)
	# todo: include field(s) for commands, only after data modeling on frontend

