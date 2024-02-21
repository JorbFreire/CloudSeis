from ..database.connection import database
from ..models.ProgramGroupModel import ProgramGroupModel
from ..models.ProgramModel import ProgramModel
from ..errors.AppError import AppError


class ProgramRepository:
    def showByGroupId(self, groupId):
        programs = ProgramModel.query.filter_by(groupId=groupId).all()
        if not programs:
            raise AppError("There are no programs for this group", 404)

        return [program.getAttributes() for program in programs]

    def create(self, groupId, newProgramData):
        programGroup = ProgramGroupModel.query.filter_by(
            id=groupId
        ).first()
        if not programGroup:
            raise AppError("Program Group does not exist", 404)

        newProgram = ProgramModel(
            name=newProgramData["name"],
            description=newProgramData["description"],
            path_to_executable_file=newProgramData["path_to_executable_file"],
            groupId=newProgramData["groupId"]
        )
        database.session.add(newProgram)
        database.session.commit()
        return newProgram.getAttributes()

    def update(self):
        pass

    def delete(self, id):
        program = ProgramModel.query.filter_by(id=id).first()
        if not program:
            raise AppError("Program does not exist", 404)

        database.session.delete(program)
        database.session.commit()
        return program.getAttributes()
