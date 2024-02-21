from ..database.connection import database
from ..models.ProgramModel import ProgramModel
from ..models.ParameterModel import ParameterModel
from ..errors.AppError import AppError


class ParameterRepository:
    def showByProgramId(self, programId):
        parameters = ParameterModel.query.filter_by(programId=programId).all()
        if not parameters:
            raise AppError("There are no parameters for this program", 404)

        return [parameter.getAttributes() for parameter in parameters]

    def create(self, programId, newParameterData):
        program = ProgramModel.query.filter_by(
            id=programId
        ).first()
        if not program:
            raise AppError("Program does not exist", 404)

        newProgram = ParameterModel(
            name=newParameterData["name"],
            description=newParameterData["description"],
            input_type=newParameterData["input_type"],
            programId=programId
        )
        database.session.add(newProgram)
        database.session.commit()
        return newProgram.getAttributes()

    def update(self):
        pass

    def delete(self, id):
        parameter = ParameterModel.query.filter_by(id=id).first()
        if not parameter:
            raise AppError("Parameter does not exist", 404)

        database.session.delete(parameter)
        database.session.commit()
        return parameter.getAttributes()
