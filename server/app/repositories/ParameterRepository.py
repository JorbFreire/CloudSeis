from ..database.connection import database
from ..models.ProgramModel import ProgramModel
from ..models.ParameterModel import ParameterModel
from ..errors.AppError import AppError


class ParameterRepository:
    def showByProgramId(self, programId: int | str) -> list[dict[str, str | int | bool]]:
        parameters = ParameterModel.query.filter_by(programId=programId).all()
        if not parameters:
            raise AppError("There are no parameters for this program", 404)

        return [parameter.getAttributes() for parameter in parameters]

    def create(self, programId: int | str) -> dict[str, str | int | bool]:
        program = ProgramModel.query.filter_by(
            id=programId
        ).first()
        if not program:
            raise AppError("Program does not exist", 404)

        newParameter = ParameterModel(
            name="",
            description="",
            examples="",
            input_type="",
            isRequired=False,
            programId=programId
        )
        database.session.add(newParameter)
        database.session.commit()
        return newParameter.getAttributes()

    def update(self, parameterId: int | str, parameterNewData: dict[str, str]) -> dict[str, str | int | bool]:
        parameter = ParameterModel.query.filter_by(
            id=parameterId
        ).first()
        if not parameter:
            raise AppError("Parameter does not exist", 404)

        parameter.name = parameterNewData["name"]
        parameter.description = parameterNewData["description"]
        parameter.example = parameterNewData["example"]
        parameter.input_type = parameterNewData["input_type"]
        parameter.isRequired = parameterNewData["isRequired"]

        database.session.commit()
        return parameter.getAttributes()

    def delete(self, id: str | int) -> dict[str, str | int | bool]:
        parameter = ParameterModel.query.filter_by(id=id).first()
        if not parameter:
            raise AppError("Parameter does not exist", 404)

        database.session.delete(parameter)
        database.session.commit()
        return parameter.getAttributes()
