import json

from ..models.ProgramModel import ProgramModel
from .get_CLI_file_path import get_CLI_file_path


def new_default_programs_from_database():
    programs = ProgramModel.query.all()
    programs_result = []
    for program_info in programs:
        programs_result.append(program_info.getAttributes())
    with open(get_CLI_file_path()) as file:
        file.write(json.dump(programs_result))
