import os
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from .plot import getPlot

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static"

@app.route("/su-file", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su')
    except Exception as e:
        return str(e)

@app.route("/su-file", methods=['POST'])
def createSuFile():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return { "file": "saved" }

@app.route("/get-plot", methods=['GET'])
def showPlotHtmlTags():
    script, div = getPlot()
    print (script)
    return jsonify({
        "script": script,
        "div": div
    })
