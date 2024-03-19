from flask import request
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from ..errors.AuthError import AuthError


private_key = "private_key"


def requireAuthentication(routeFunction):
    def wrapper(*args, **kwargs):
        userId = kwargs.get('userId')
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
        except Exception:
            raise AuthError()

        if userId != payload.get('id'):
            raise AuthError()

        response = routeFunction(*args, **kwargs)
        return response
    return wrapper
