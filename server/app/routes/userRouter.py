from flask import Blueprint, request, jsonify

from ..repositories.UserRepository import UserRepository

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()

@userRouter.route("/show", methods=['GET'])
def showUser(userId):
    user = userRepository.show(userId)
    return jsonify({ user })

@userRouter.route("/create", methods=['POST'])
def createUser():
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    newUser = userRepository.create(data.user)
    return jsonify({ newUser })

@userRouter.route("/update", methods=['PUT'])
def updateUser(userId):
    data = request.get_json()
    if data == None:
        return jsonify(
            {"Error": "No body"}, 
            status=400
        )
    updatedUser = userRepository.update(userId, data.user)
    return jsonify({ updatedUser })

@userRouter.route("/delete", methods=['DELETE'])
def deleteUser(userId):
    user = userRepository.delete(userId)
    return jsonify({ user })

