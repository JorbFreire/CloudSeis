from typing import Literal
from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError

from .config.database import migrations_root_path, get_db_uri
from .config.upload import upload_folder
from .database.connection import database, migrate

from .routes import router
from .errors.AppError import AppError
from .errors.AuthError import AuthError
from .errors.FileError import FileError

from .cli import populate_database_programs, new_default_programs_from_database, write_programs_docs


def create_app(mode: Literal["production", "development", "test"] = "development"):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(mode)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)
    migrate.init_app(app, database, migrations_root_path)

    if mode == "test":
        app.config.update({
            "TESTING": True,
        })

    app.register_blueprint(router)
    CORS(app)

    @app.errorhandler(ValidationError)
    def handle_validation_exception(error):
        return jsonify({"Error": error.messages_dict}), 422

    @app.errorhandler(AppError)
    def handle_app_exception(error):
        return jsonify({"Error": error.message}), error.statusCode

    @app.errorhandler(AuthError)
    def handle_auth_exception(error):
        message = "Not authorized"
        if mode == "development":
            message = error.message
        # *** status code 403 means that it requires admin role
        return jsonify({"Error": message}), error.statusCode

    @app.errorhandler(AppError)
    def handle_file_exception(error):
        return jsonify({"Error": error.message}), error.statusCode

    app.register_error_handler(ValidationError, handle_validation_exception)
    app.register_error_handler(AppError, handle_app_exception)
    app.register_error_handler(AuthError, handle_auth_exception)
    app.register_error_handler(FileError, handle_file_exception)

    @app.cli.command('write_su_programs')
    @app.cli.command('ws')
    def write_programs():
        write_programs_docs.write_programs_docs()
    @app.cli.command('populate-programs')
    @app.cli.command('pp')
    def populate_programs():
        populate_database_programs() # HOW??

    @app.cli.command('export-programs')
    @app.cli.command('ep')
    def new_default_programs():
        new_default_programs_from_database()

    return app
