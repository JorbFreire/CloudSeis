from flask import Blueprint, request, jsonify

from ..repositories.UserRepository import UserRepository
from ..errors.AppError import AppError

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()


@userRouter.route("/list", methods=['GET'])
def listUsers():
    users = userRepository.showAll()
    return jsonify(users)


@userRouter.route("/show/<userId>", methods=['GET'])
def showUser(userId):
    user = userRepository.showById(userId)
    return jsonify(user)


@userRouter.route("/create", methods=['POST'])
def createUser():
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    newUser = userRepository.create(data)
    return jsonify(newUser)


@userRouter.route("/update/<userId>", methods=['PUT'])
def updateUser(userId):
    data = request.get_json()
    if data == None:
        raise AppError("No body", 400)

    updatedUser = userRepository.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete/<userId>", methods=['DELETE'])
def deleteUser(userId):
    user = userRepository.delete(userId)
    return jsonify(user)

