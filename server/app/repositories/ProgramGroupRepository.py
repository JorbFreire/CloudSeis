from ..database.connection import database
from ..models.ProgramGroupModel import ProgramGroupModel
from ..errors.AppError import AppError


class ProgramGroupRepository:
    def listAll(self) -> list[dict[str, str]]:
        programGroups = ProgramGroupModel.query.all()
        if not programGroups:
            raise AppError("There are no program groups created", 404)

        return [programGroup.getAttributes() for programGroup in programGroups]

    def create(self, newGroupData: dict[str, str]) -> dict[str, str]:
        newProgramGroup = ProgramGroupModel(
            name=newGroupData["name"],
            description=newGroupData["description"] if newGroupData["description"] else ""
        )
        database.session.add(newProgramGroup)
        database.session.commit()
        return newProgramGroup.getAttributes()

    def update(self, id: str | int, newGroupData: dict[str, str]) -> dict[str, str]:
        programGroup = ProgramGroupModel.query.filter_by(id=id).first()

        if not programGroup:
            raise AppError("Group does not exist", 404)

        programGroup.name = newGroupData["name"]
        programGroup.description = newGroupData["description"]

        database.commit()
        return programGroup.getAttributes()

    def delete(self, id: str | int) -> dict[str, str]:
        programGroup = ProgramGroupModel.query.filter_by(id=id).first()
        if not programGroup:
            raise AppError("Group does not exist", 404)

        database.session.delete(programGroup)
        database.session.commit()
        return programGroup.getAttributes()
