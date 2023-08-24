import sqlalchemy as dbTypes
from sqlalchemy import select


from ..database.connection import database
from .CommandModel import CommandModel


class OrderedCommandsListModel(database.Model):  # type: ignore
    __tablename__ = "ordered_commands_list_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)

    workflowId = dbTypes.Column(dbTypes.ForeignKey(
        "workflows_table.id",
        name="FK_workflows_table_workflow_commands_list_table"
    ))

    # ! thats a huge workarround, but should work
    # each integer represents an id on command table
    # that way will be easy to keep the list of commands ordered
    commandIds = dbTypes.Column(dbTypes.ARRAY(dbTypes.Integer))

    def getCommands(self) -> list[dict[str, str]]:
        if not self.commandsIds[0]:
            return []
        commands = CommandModel.query.filter(
            CommandModel.id.in_(self.commandIds)
        )
        return commands

    def getAttributes(self) -> dict[str, str | list[int]]:
        return {
            "id": self.id,
            "workflowId": self.workflowId,
            "commandIds": self.commandIds
        }
