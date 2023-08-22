import sqlalchemy as dbTypes

from ..database.connection import database


class CommandModel(database.Model):  # type: ignore
    __tablename__ = "commands_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    # stringfied JSON
    parameters = dbTypes.Column(dbTypes.Text)

    workflowId = dbTypes.Column(dbTypes.ForeignKey(
        "workflows_table.id",
        name="FK_workflows_table_commands_table"
    ))

    def getAttributes(self) -> dict[str, str]:
        return {
            "id": self.id,
            "workflowId": self.workflowId,
            "name": self.name,
            "parameters": self.parameters
        }
