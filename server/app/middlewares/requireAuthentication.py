from uuid import UUID

from flask import request
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from ..models.UserModel import UserModel
from ..errors.AuthError import AuthError


private_key = "private_key"


def requireAuthentication(routeFunction, routeModel=None, isAdminRequired=False):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthError("No token")

        token = token.replace("Bearer ", "")

        try:
            payload = decode(token, key=private_key, algorithms=["HS256"])
        except InvalidSignatureError:
            raise AuthError("Invalid Token Signature")
        except ExpiredSignatureError:
            raise AuthError("Expired Token")
        except:
            raise AuthError()

        userId = payload["id"]
        user = UserModel.query.filter_by(id=UUID(userId)).first()

        if isAdminRequired and not user.is_admin:
            raise AuthError("Must be admin")

        # Really bad implementation
        if routeModel:
            modelId = int(list(kwargs.values())[0])
            modelObject = routeModel.query.filter_by(id=modelId).first()
            if not modelObject:
                raise AuthError("No instance found with this Id") # change message
            userAttr = modelObject.owner_email if hasattr(modelObject, 'owner_email') else modelObject.userId
            if userAttr != user.email and userAttr != user.id:
                raise AuthError("Unauthorized by required auth")  # change message


        # *** "payload.id" will be the first argument of any function
        # *** using "requireAuthentication" as decorator
        response = routeFunction(userId, *args, **kwargs)
        return response
    return wrapper
