import sqlalchemy as dbTypes

from ..database.connection import database


class FileLinkModel(database.Model):  # type: ignore
    __tablename__ = "file_link_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    #! maybe change to "name" to "path"
    name = dbTypes.Column(dbTypes.String)
    # *** stack || shotgather_ep || ...
    data_type = dbTypes.Column(dbTypes.String)

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_projects_table_file_link_table"
    ))

    created_at = dbTypes.Column(
        dbTypes.DateTime(timezone=True),
        server_default=dbTypes.func.now()
    )
    modified_at = dbTypes.Column(
        dbTypes.DateTime(timezone=True),
        onupdate=dbTypes.func.now()
    )
