from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..serializers.UserSerializer import UserCreateSchema, UserUpdateSchema
from ..repositories.UserRepository import UserRepository

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")
userRepository = UserRepository()


# todo:
# encrypty password

@userRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=UserCreateSchema)
def createUser():
    data = request.get_json()

    newUser = userRepository.create(data)
    return jsonify(newUser)


# *** debug route, could be turned of on production
@userRouter.route("/list", methods=['GET'])
def listUsers():
    users = userRepository.showAll()
    return jsonify(users)


# *** maybe also a debug function that could be turned of on production ***
@userRouter.route("/show/<userId>", methods=['GET'])
def showUser(userId):
    user = userRepository.showById(userId)
    return jsonify(user)


@userRouter.route("/update", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=UserUpdateSchema)
@decorator_factory(requireAuthentication)
def updateUser(userId):
    data = request.get_json()
    updatedUser = userRepository.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete", methods=['DELETE'])
@decorator_factory(requireAuthentication)
def deleteUser(userId):
    user = userRepository.delete(userId)
    return jsonify(user)

# Route for test
@userRouter.route("/test", methods=['POST'])
def test():
    data = request.get_json()
    user = userRepository.testCreation(data)

    return jsonify(user)
