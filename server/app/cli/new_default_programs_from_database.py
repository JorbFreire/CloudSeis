import json

from ..models.ProgramModel import ProgramModel


def new_default_programs_from_database():
    programs = ProgramModel.query.all()
    programs_result = []
    for program_info in programs:
        programs_result.append(program_info.getAttributes())
    with open("./default_programs.json") as file:
        file.write(json.dump(programs_result))
