from uuid import UUID

from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel
from ..errors.AppError import AppError


class LineRepository:
    def showByProjectId(self, projectId: str | int) -> list[dict[str, str | list[dict[str, str]]]]:
        lines = LineModel.query.filter_by(projectId=projectId).all()
        if not lines:
            raise AppError("There are no Lines for this project", 404)

        return [line.getAttributes() for line in lines]

    def create(self, userId: str, projectId: str | int, newLineName: str) -> dict[str, str]:
        project = ProjectModel.query.filter_by(
            id=projectId
        ).first()
        if not project:
            raise AppError("Project does not exist", 404)

        user = UserModel.query.filter_by(id=UUID(userId)).first()

        newLine = LineModel(
            name=newLineName,
            projectId=project.id,
            owner_email=user.email
        )

        database.session.add(newLine)
        database.session.commit()
        return newLine.getAttributes()

    def update(self, id: str | int, newLineData: str) -> dict[str, str]:
        line = LineModel.query.filter_by(id=id).first()
        if not line:
            raise AppError("Line does not exist", 404)

        line.name = newLineData
        database.session.commit()

        return line.getAttributes()

    def delete(self, id: str | int) -> dict[str, str]:
        line = LineModel.query.filter_by(id=id).first()
        if not line:
            raise AppError("Line does not exist", 404)

        database.session.delete(line)
        database.session.commit()
        return line.getAttributes()

    # DEBUG METHOD
    def listAllDebug(self) -> list[dict[str, str]]:
        lines = LineModel.query.all()
        return [line.getAttributes() for line in lines]
