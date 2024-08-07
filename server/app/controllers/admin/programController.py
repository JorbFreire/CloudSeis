from types import SimpleNamespace

from ...database.connection import database
from ...models.ProgramGroupModel import ProgramGroupModel
from ...models.ProgramModel import ProgramModel
from ...errors.AppError import AppError


def showByGroupId(groupId):
    programs = ProgramModel.query.filter_by(groupId=groupId).all()
    if not programs:
        raise AppError("There are no programs for this group", 404)

    return [program.getAttributes() for program in programs]


def create(groupId, newProgramData):
    programGroup = ProgramGroupModel.query.filter_by(
        id=groupId
    ).first()
    if not programGroup:
        raise AppError("Program Group does not exist", 404)

    newProgram = ProgramModel(
        name=newProgramData["name"],
        description=newProgramData["description"],
        path_to_executable_file=newProgramData["path_to_executable_file"],
        groupId=groupId
    )
    database.session.add(newProgram)
    database.session.commit()
    return newProgram.getAttributes()


def update(programId, programNewData):
    program = ProgramModel.query.filter_by(
        id=programId
    ).first()
    if not program:
        raise AppError("Program does not exist", 404)

    programNewData.name = programNewData["name"]
    programNewData.description = programNewData["description"]
    programNewData.path_to_executable_file = programNewData["path_to_executable_file"]
    programNewData.groupId = programNewData["groupId"]

    database.session.commit()
    return program.getAttributes()


def delete(id):
    program = ProgramModel.query.filter_by(id=id).first()
    if not program:
        raise AppError("Program does not exist", 404)

    database.session.delete(program)
    database.session.commit()
    return program.getAttributes()


programController = SimpleNamespace(
    showByGroupId=showByGroupId,
    create=create,
    update=update,
    delete=delete,
)
