from flask import Blueprint, send_file, request, jsonify

from .repositories.PlotRepository import PlotRepository
from .repositories.SeismicFileRepository import SeismicFileRepository

router = Blueprint("routes", __name__)

plotRepository = PlotRepository()
seismicFileRepository = SeismicFileRepository()

@router.route("/su-file", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su')
    except Exception as error:
        return str(error)


@router.route("/su-file", methods=['POST'])
def createSuFile():
    file = request.files['file']
    unique_filename = seismicFileRepository.create(file)
    return { "unique_filename": unique_filename }


@router.route("/su-file/<unique_filename>/filters", methods=['PUT'])
def updateSuFile(unique_filename):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )

    updateOptions = data["updateOptions"]
    process_output = seismicFileRepository.update(unique_filename, updateOptions)
    return jsonify({
        "process_output": process_output
    })
 

@router.route("/get-plot/<unique_filename>", methods=['GET'])
def showPlotHtmlTags(unique_filename):
    script, div = plotRepository.show(unique_filename)
    return jsonify({
        "script": script,
        "div": div
    })
