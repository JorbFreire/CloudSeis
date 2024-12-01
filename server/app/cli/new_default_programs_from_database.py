import json

from ..models.ProgramModel import ProgramModel
from .get_CLI_file_path import get_CLI_file_path
from ..create_app import create_app

def new_default_programs_from_database():
    app = create_app("development")
    with app.app_context():
        try:
            programs = ProgramModel.query.all()
            programs_result = [program.getAttributes() for program in programs]

            cli_file_path = get_CLI_file_path()
            with open(cli_file_path, 'w') as file:
                json.dump(programs_result, file, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    new_default_programs_from_database()
