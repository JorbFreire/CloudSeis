from flask import Blueprint, request, jsonify

from ..repositories.UserRepository import UserRepository
from ..errors.AppError import AppError
from ..validations.userValidation import validateData, emailRegex, passwordRegex
from ..validations.tokenValidation import generateToken, verifyToken, private_key

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()

token = None

@userRouter.route("/login", methods=['GET'])
def loginUser():
    data = request.get_json()
    if not validateData("email", "password", data=data):
        raise AppError("Invalid body or data", 400)

    user = userRepository.login(data["email"], data["password"])
    global token
    token = generateToken(data, private_key)
    return jsonify(user.getAttributes())


@userRouter.route("/logout/<userId>", methods=['GET'])
def logoutUser(userId):
    data = request.get_json()
    if not validateData("password", data=data):
        raise AppError("Invalid body or data", 400)

    global token
    if not verifyToken(token, private_key):
        raise AppError("Unauthorized", 401)

    user = userRepository.logout(userId, data["password"])
    token = None
    return jsonify(user.getAttributes())


@userRouter.route("/create", methods=['POST'])
def createUser():
    data = request.get_json()

    if not validateData("name", "email", "password", data=data):
        raise AppError("Invalid body or data", 400)
    if not emailRegex(data["email"]):
        raise AppError("Invalide email", 400)
    if not passwordRegex(data["password"]):
        raise AppError("Invalid password", 400)

    newUser = userRepository.create(data)
    global token
    token = generateToken(data, private_key)
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
def updateUser(userId):
    data = request.get_json()

    global token
    if not verifyToken(token, private_key):
        raise AppError("Unauthorized", 401)

    updatedUser = userRepository.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete/<userId>", methods=['DELETE'])
def deleteUser(userId):
    global token
    if not verifyToken(token, private_key):
        raise AppError("Unauthorized", 401)

    user = userRepository.delete(userId)
    return jsonify(user)
