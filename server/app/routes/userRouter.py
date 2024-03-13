from flask import Blueprint, request, jsonify

from ..repositories.UserRepository import UserRepository
from ..errors.AppError import AppError
from ..validations.userValidation import validateData, emailRegex, passwordRegex
from ..validations.tokenValidation import generateToken, verifyToken, private_key

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()


# todo:
# verify user and its token feature
# encrypty password

@userRouter.route("/login", methods=['GET'])
def loginUser():
    data = request.get_json()
    if not validateData("email", "password", data=data):
        raise AppError("Invalid body or data", 400)

    userRepository.login(data["email"], data["password"])
    token = generateToken(data, private_key)
    return jsonify(token)


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
    token = request.headers.get('Authorization')
    token = str(token).replace("Bearer ", "")

    if not verifyToken(token, private_key):
        raise AppError("Unauthorized", 401)

    updatedUser = userRepository.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete/<userId>", methods=['DELETE'])
def deleteUser(userId):
    token = request.headers.get('Authorization')
    token = str(token).replace("Bearer ", "")

    if not verifyToken(token, private_key):
        raise AppError("Unauthorized", 401)

    user = userRepository.delete(userId)
    return jsonify(user)
