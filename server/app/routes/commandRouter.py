from flask import Blueprint, request, jsonify

from ..repositories.CommandRepository import CommandRepository

commandRouter = Blueprint(
    "command-routes",
    __name__,
    url_prefix="/command"
)
commandRepository = CommandRepository()


@commandRouter.route("/show", methods=['GET'])
def showCommand(id):
    command = commandRepository.show(id)
    return jsonify({command})


@commandRouter.route("/create", methods=['POST'])
def createCommand():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    newCommand = commandRepository.create(data.command)
    return jsonify({newCommand})


@commandRouter.route("/update", methods=['PUT'])
def updateCommand(id):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"},
            status=400
        )
    updatedCommand = commandRepository.update(id, data.command)
    return jsonify({updatedCommand})


@commandRouter.route("/delete", methods=['DELETE'])
def deleteCommand(id):
    command = commandRepository.delete(id)
    return jsonify({command})
