from flask import Blueprint, request, jsonify

from ..repositories.UserRepository import UserRepository
from ..errors.AppError import AppError
from ..validations.userValidation import validateData, credentialsRegex
from ..middlewares.requireAuthentication import requireAuthentication

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()


# todo:
# encrypty password

@userRouter.route("/create", methods=['POST'])
def createUser():
    data = request.get_json()

    validateData("name", "email", "password", data=data)
    credentialsRegex(data["email"], data["password"])

    newUser = userRepository.create(data)
    return jsonify(newUser)


@userRouter.route("/list", methods=['GET'])
def listUsers():
    users = userRepository.showAll()
    return jsonify(users)


@userRouter.route("/show/<userId>", methods=['GET'])
def showUser(userId):
    user = userRepository.showById(userId)
    return jsonify(user)


@userRouter.route("/update/<userId>", methods=['PUT'])
@requireAuthentication
def updateUser(userId):
    data = request.get_json()

    updatedUser = userRepository.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete/<userId>", methods=['DELETE'])
@requireAuthentication
def deleteUser(userId):
    user = userRepository.delete(userId)
    return jsonify(user)
