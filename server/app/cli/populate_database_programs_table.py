import json

from ..models.ProgramModel import ProgramModel
from ..models.ParameterModel import ParameterModel
from ..database.connection import database

programsArray = []
with open("./default_programs.json") as file:
    programsArray = json.loads(file.read())


def populate_database_paremeters_table():
    default_programs_parameters = []

    for program_info in programsArray:
        programFromDataBase = ProgramModel.query.filter_by(
            name=program_info["name"]
        ).first()
        programId = programFromDataBase["id"]

        for parameter_info in programsArray:
            default_programs_parameters.append(
                ParameterModel(
                    name=parameter_info["name"],
                    description=parameter_info["description"],
                    input_type=parameter_info["input_type"],
                    programId=programId,
                )
            )

    database.session.bulk_save_objects(default_programs_parameters)
    database.session.commit()


def populate_database_programs_table():
    # repository methods
    # [x] create program
    # [] create parameter (gets program id)
    # [] get programs
    # workflow for this method:
    # -> json_programs.map: p => create program(p)
    # -> get programs
    # -> programs.map: p => json_parameters[p.name].map: parameter => create parameter(p.id, parameter)
    if ProgramModel.query.count() == 0:
        # * Create default rows *
        # * "default_programs" are usually Seismic Unix programs *
        # todo: use "getCWD" and/or related to abstract

        default_programs = []
        for program_info in programsArray:
            default_programs.append(
                ProgramModel(
                    name=program_info["name"],
                    description=program_info["description"],
                    path_to_executable_file=program_info["path_to_executable_file"]
                )
            )

        database.session.bulk_save_objects(default_programs)
        database.session.commit()

        populate_database_paremeters_table()
        print("Default programs insert into the database")
    else:
        print("Database programs table already initialized")
