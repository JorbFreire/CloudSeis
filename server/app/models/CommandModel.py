import sqlalchemy as dbTypes

from ..database.connection import database


class CommandModel(database.Model):  # type: ignore
    __tablename__ = "commands_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    # *** stringfied JSON
    parameters = dbTypes.Column(dbTypes.Text)

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_commands_table"
    ))

    program_id = dbTypes.Column(dbTypes.ForeignKey(
        "programs_table.id",
        name="FK_programs_table_commands_table"
    ))

    workflowId = dbTypes.Column(dbTypes.ForeignKey(
        "workflows_table.id",
        name="FK_workflows_table_commands_table"
    ))

    def getAttributes(self) -> dict[str, str]:
        return {
            "id": self.id,
            "program_id": self.program_id,
            "workflowId": self.workflowId,
            "name": self.name,
            "parameters": self.parameters
        }
