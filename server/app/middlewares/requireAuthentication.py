from flask import request
from jwt import decode
# ! on production this erros should have less details
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from ..errors.AuthError import AuthError


private_key = "private_key"


def requireAuthentication(routeFunction):
    def wrapper(*args, **kwargs):
        userId = kwargs.get('userId')
        token = request.headers.get('Authorization')
        token = str(token).replace("Bearer ", "")

        if not token:
            raise AuthError("No token", 404)

        try:
            payload = decode(token, key=private_key, algorithms=["HS256"])
        except InvalidSignatureError as e:
            raise AuthError("Invalid Token Signature")
        except ExpiredSignatureError as e:
            raise AuthError("Expired Token")
        except Exception as e:
            raise AuthError()

        if userId != payload.get('id'):
            raise AuthError()

        response = routeFunction(*args, **kwargs)
        return response
    return wrapper
