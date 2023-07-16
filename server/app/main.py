from flask import Flask
from flask_cors import CORS

from .routes import router

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static"

app.register_blueprint(router)
