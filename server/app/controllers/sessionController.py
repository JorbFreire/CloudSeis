from types import SimpleNamespace

from jwt import encode

from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel
from ..hash.hash import checkPassword
from ..config.private_key import private_key


def createSession(email, password) -> str:
    user = UserModel.query.filter_by(email=email).first()
    if not user or not checkPassword(password, user.password):
        raise AuthError("Invalid email or password")

    try:
        token = encode(
            payload=user.getAttributes(),
            key=private_key,
            algorithm="HS256"
        )
    except:
        raise AuthError("Could not generate token")

    return {"token": token}


def validateSession(token: str):
    payload = validateSession(token)
    return payload


def revalidateSession():
    # todo: revalidateSession shall be implemented but is not a priority
    pass


sessionController = SimpleNamespace(
    createSession=createSession,
    validateSession=validateSession,
    revalidateSession=revalidateSession,
)
