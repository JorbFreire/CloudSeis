from flask import Blueprint, send_file, request, jsonify

from ..repositories.FileRepository import FileRepository

suFileRouter = Blueprint("su-file-routes", __name__, url_prefix="/su-file")
fileRepository = FileRepository()

# ? note sure if this "/ should be keep or not"
@suFileRouter.route("/", methods=['GET'])
def showSuFile():
    try:
        return send_file('../static/marmousi_CS.su') # Faz o download ??
    except Exception as error:
        return str(error)


# ? note sure if this "/ should be keep or not"
@suFileRouter.route("/", methods=['POST'])
def createSuFile():
    file = request.files['file']
    unique_filename = fileRepository.create(file)
    return {"unique_filename": unique_filename}


@suFileRouter.route("/<unique_filename>/filters", methods=['PUT'])
def updateSuFile(unique_filename):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )

    seismicUnixCommandsQueue = data["seismicUnixCommandsQueue"]
    process_output = fileRepository.update(unique_filename, seismicUnixCommandsQueue)
    return jsonify({
        "process_output": process_output
    })
