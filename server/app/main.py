from .create_app import create_app
from dotenv import load_dotenv

from .cli import populate_database_programs_table, new_default_programs_from_database


if __name__ == "main":
    load_dotenv()
    app = create_app("development")

    app.run(debug=True)
