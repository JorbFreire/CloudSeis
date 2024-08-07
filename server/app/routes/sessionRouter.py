from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import sessionController
from ..serializers.SessionSerializer import SessionCreateSchema

sessionRouter = Blueprint("session-routes", __name__, url_prefix="/session")


@sessionRouter.route("/", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=SessionCreateSchema)
def create():
    data = request.get_json()

    token = sessionController.createSession(data["email"], data["password"])
    return jsonify(token)


@sessionRouter.route("/validate/<token>", methods=['POST'])
def create(token):
    sessionController.validateSession(token)
    return ('', 200)
