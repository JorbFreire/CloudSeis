import os
from flask import Flask, send_file, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static"

@app.route("/su-file", methods=['GET'])
def showSuFile():
    try:
        return send_file('static/mamousi.su', attachment_filename='mamousi.su')
    except Exception as e:
        return str(e)

@app.route("/su-file", methods=['POST'])
def createSuFile():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return { "file": "saved" }
