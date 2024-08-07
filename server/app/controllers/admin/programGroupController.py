from types import SimpleNamespace

from ...database.connection import database
from ...models.ProgramGroupModel import ProgramGroupModel
from ...errors.AppError import AppError


def listAll():
    programGroups = ProgramGroupModel.query.all()
    if not programGroups:
        raise AppError("There are no program groups created", 404)

    return [programGroup.getAttributes() for programGroup in programGroups]


def create(newGroupData):
    newProgramGroup = ProgramGroupModel(
        name=newGroupData["name"],
        description=newGroupData["description"] if newGroupData["description"] else ""
    )
    database.session.add(newProgramGroup)
    database.session.commit()
    return newProgramGroup.getAttributes()


def update():
    pass


def delete(id):
    programGroup = ProgramGroupModel.query.filter_by(id=id).first()
    if not programGroup:
        raise AppError("Group does not exist", 404)

    database.session.delete(programGroup)
    database.session.commit()
    return programGroup.getAttributes()


programGroupController = SimpleNamespace(
    listAll=listAll,
    create=create,
    update=update,
    delete=delete,
)
