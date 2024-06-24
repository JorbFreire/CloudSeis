import sqlalchemy as dbTypes


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
        if len(self.commandIds) == 0:
            return []
        commands = []
        for id in self.commandIds:
            command = CommandModel.query.filter_by(
                id=id
            ).first()
            commands.append(command)

        # return [command.getAttributes() for command in commands]
        return commands

    def getAttributes(self) -> dict[str, str | list[int]]:
        return {
            "id": self.id,
            "workflowId": self.workflowId,
            "commandIds": self.commandIds
        }
