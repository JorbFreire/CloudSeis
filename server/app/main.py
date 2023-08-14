from flask import Flask, jsonify
from flask_cors import CORS
from os import path, getcwd

from .database.connection import database, migrate
from .routes import router
from .errors.AppError import AppError

database_root_path = path.join(getcwd(), 'app/database')
migrations_root_path = path.join(database_root_path, 'migrations')

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + path.join(database_root_path, 'db.sqlite3') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)
migrate.init_app(app, database, migrations_root_path)

app.register_blueprint(router)


@app.errorhandler(AppError)
def handle_app_exception(error):
  return jsonify({ "Error": error.message }), error.statusCode
app.register_error_handler(AppError, handle_app_exception)


if __name__ == "main":
  app.run(debug=True)

