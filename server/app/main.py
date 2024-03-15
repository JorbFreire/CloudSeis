from create_app import create_app

from .cli import populate_database_programs_table, new_default_programs_from_database

if __name__ == "main":
    app = create_app("development")

    @app.cli.command('populate-programs')
    def populate_programs():
        populate_database_programs_table()

    @app.cli.command('update-default-programs-file')
    def new_default_programs():
        new_default_programs_from_database()

    app.run(debug=True)
