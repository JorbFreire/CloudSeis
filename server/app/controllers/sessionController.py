from types import SimpleNamespace

from jwt import encode

from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel
from ..config.private_key import private_key

from ..services.passwordServices import checkPassword
from ..services.validateToken import validateToken


def create(email, password) -> str:
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


def validate(token: str):
    payload = validateToken(token)
    return payload


def revalidate():
    # todo: revalidateSession shall be implemented but is not a priority
    pass


sessionController = SimpleNamespace(
    create=create,
    validate=validate,
    revalidate=revalidate,
)
