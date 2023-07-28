from flask import Blueprint, send_file, request, jsonify

from ..repositories.SeismicFileRepository import SeismicFileRepository

suFileRouter = Blueprint("su-file-routes", __name__, url_prefix="/su-file")
seismicFileRepository = SeismicFileRepository()

# ? note sure if this "/ should be keep or not" 
@suFileRouter.route("/", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su')
    except Exception as error:
        return str(error)


# ? note sure if this "/ should be keep or not" 
@suFileRouter.route("/", methods=['POST'])
def createSuFile():
    file = request.files['file']
    unique_filename = seismicFileRepository.create(file)
    return { "unique_filename": unique_filename }


@suFileRouter.route("/<unique_filename>/filters", methods=['PUT'])
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

