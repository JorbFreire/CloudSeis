import sqlalchemy as dbTypes

from ..database.connection import database


class ProgramModel(database.Model):  # type: ignore
    __tablename__ = "programs_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    description = dbTypes.Column(dbTypes.String)
    path_to_executable_file = dbTypes.Column(dbTypes.String)
    # create "groups_table" and relate it

    def getAttributes(self) -> dict[str, str | dict[str, str]]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "path_to_executable_file": self.path_to_executable_file,
        }
