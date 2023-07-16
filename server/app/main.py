from flask import Flask
from flask_cors import CORS

from .database.connection import database
from .routes import router


app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(router)


if __name__ == "main":
  database.init_app(app=app)
  with app.test_request_context():
    database.create_all()
  app.run(debug=True)

