from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.validateRequestBody import validateRequestBody

from ..repositories.SessionRepository import SessionRepository
from ..serializers.SessionSerializer import SessionCreateSchema

sessionRouter = Blueprint("session-routes", __name__, url_prefix="/session")
sessionRepository = SessionRepository()


@sessionRouter.route("/", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=SessionCreateSchema)
def create():
    data = request.get_json()

    token = sessionRepository.login(data["email"], data["password"])
    return jsonify(token)
