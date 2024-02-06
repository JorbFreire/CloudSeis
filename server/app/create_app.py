from flask.cli import AppGroup
from typing import Literal
from flask import Flask, jsonify
from flask_cors import CORS

from .config.database import migrations_root_path, get_db_uri
from .config.upload import upload_folder
from .database.connection import database, migrate

from .routes import router
from .errors.AppError import AppError


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

    @app.errorhandler(AppError)
    def handle_app_exception(error):
        return jsonify({"Error": error.message}), error.statusCode

    app.register_error_handler(AppError, handle_app_exception)
    return app
