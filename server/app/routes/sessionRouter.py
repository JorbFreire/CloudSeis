from flask import Blueprint, request, jsonify
from ..repositories.SessionRepository import SessionRepository

sessionRouter = Blueprint("session-routes", __name__, url_prefix="/session")
sessionRepository = SessionRepository()


@sessionRouter.route("/", methods=['POST'])
def create():
    data = request.get_json()

    token = sessionRepository.createSession(data["email"], data["password"])
    return jsonify(token)
