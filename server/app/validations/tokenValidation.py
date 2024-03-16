from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from logging import error

from ..errors.AppError import AppError

private_key = "private_key"

def generateToken(payload: dict) -> str | None:
    try:
        token = encode(payload=payload, key=private_key, algorithm="HS256")
    except Exception as e:
        error(f"Unexpected error during token generation: {e}")
        return None

    return token

def verifyToken(token, id) -> AppError | None:
    if not token:
        raise AppError("No token", 404)

    try:
        payload = decode(token, key=private_key, algorithms=["HS256"])
    except InvalidSignatureError as e:
        error(f"Failed in token verification: {e}")
        raise AppError("Invalid Token Signature", 401)
    except ExpiredSignatureError as e:
        error(f"Token out of validation {e}")
        raise AppError("Expired Token", 401)
    except Exception as e:
        error(f"Unexpected error during token verification: {e}")
        raise AppError("Unauthorized", 401)

    if id != payload.get('id'):
        raise AppError("Unauthorized", 401)
