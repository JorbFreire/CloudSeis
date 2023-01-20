import os
from flask import Flask, send_file, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static"

@app.route("/su-file", methods=['GET'])
def showSuFile():
    try:
        return send_file('static/marmousi_CS.su')
    except Exception as e:
        return str(e)

@app.route("/su-file", methods=['POST'])
def createSuFile():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return { "file": "saved" }

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
