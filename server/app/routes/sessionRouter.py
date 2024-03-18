from flask import Blueprint, request, jsonify
from ..repositories.SessionRepository import SessionRepository

sessionRouter = Blueprint("session-routes", __name__, url_prefix="/session")
sessionRepository = SessionRepository()


@sessionRouter.route("/", methods=['GET'])
def create():
    data = request.get_json()

    token = sessionRepository.login(data["email"], data["password"])
    return jsonify(token)
