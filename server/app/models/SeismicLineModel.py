import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .SeismicWorkflowModel import SeismicWorkflowModel


class SeismicLineModel(database.Model): # type: ignore
	__tablename__ = "seismic_lines_table"

	id = dbTypes.Column(dbTypes.Integer, primary_key=True)
	name = dbTypes.Column(dbTypes.String)

	seismicProjectId = dbTypes.Column( dbTypes.ForeignKey( \
		"seismic_projects_table.id", \
		name="FK_seismic_projects_table_seismic_lines_table" \
	))
	seismicWorkflows: Mapped[List[SeismicWorkflowModel]] = relationship(SeismicWorkflowModel)

