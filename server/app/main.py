import os
from datetime import datetime
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

    unique_filename = file.filename.replace(".su", "_").replace(" ", "_")
    unique_filename = unique_filename + datetime.now().strftime("%d%m%Y_%H%M%S") + ".su"

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    return { "unique_filename": unique_filename }

@app.route("/get-plot/<unique_filename>", methods=['GET'])
def showPlotHtmlTags(unique_filename):
    script, div = getPlot(unique_filename)
    return jsonify({
        "script": script,
        "div": div
    })
