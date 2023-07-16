
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

from .repositories.PlotRepository import PlotRepository
from .repositories.SeismicFileRepository import SeismicFileRepository

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static"

plotRepository = PlotRepository()
seismicFileRepository = SeismicFileRepository()

@app.route("/su-file", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su')
    except Exception as e:
        return str(e)


@app.route("/su-file", methods=['POST'])
def createSuFile():
    file = request.files['file']
    unique_filename = seismicFileRepository.create(file, app)
    return { "unique_filename": unique_filename }


@app.route("/su-file/<unique_filename>/filters", methods=['PUT'])
def updateSuFile(unique_filename):
    data = request.get_json()
    updateOptions = data["updateOptions"]
    process_output = seismicFileRepository.update(unique_filename, updateOptions)
    return jsonify({
        "process_output": process_output
    })
 

@app.route("/get-plot/<unique_filename>", methods=['GET'])
def showPlotHtmlTags(unique_filename):
    script, div = plotRepository.show(unique_filename)
    return jsonify({
        "script": script,
        "div": div
    })
