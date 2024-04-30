from uuid import UUID

from flask import request

from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel

from ..models.UserModel import UserModel
from ..errors.AuthError import AuthError

from ..repositories.SessionRepository import SessionRepository


sessionRepository = SessionRepository()

# Line creation returns error with wrong token
# Not finding line from workflow creation root
# Email not matchin when references projectId for workflow creation root


def requireAuthentication(routeFunction, routeModel=None, isAdminRequired=False):
    def wrapper(routeModel=routeModel, *args, **kwargs):
        token = request.headers.get('Authorization')
        hasData = False
        data = {}

        if not token:
            raise AuthError("No token")

        if (request.method == "post" or request.method == "put"):
            hasData = True

        if (hasData):
            data = request.get_json()

        payload = sessionRepository.validateSession()

        userId = payload["id"]
        user = UserModel.query.filter_by(id=UUID(userId)).first()

        if isAdminRequired and not user.is_admin:
            raise AuthError("Must be admin")

        # Really bad implementation
        if (not routeModel) and ("parentType" in data):
            routeModel = LineModel if data["parentType"] == "lineId" else ProjectModel

        if routeModel:
            modelId = int(list(kwargs.values())[0])
            modelObject = routeModel.query.filter_by(id=modelId).first()

            if not modelObject:
                raise AuthError("No instance found with this Id")

            userAttr = modelObject.owner_email if hasattr(
                modelObject, 'owner_email'
            ) else modelObject.userId
            if userAttr != user.email and userAttr != user.id:
                raise AuthError("Unauthorized by required auth")

        # *** "payload.id" will be the first argument of any function
        # *** using "requireAuthentication" as decorator
        response = routeFunction(userId, *args, **kwargs)
        return response
    return wrapper
