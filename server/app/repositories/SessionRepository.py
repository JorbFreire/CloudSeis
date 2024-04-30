from jwt import encode

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel
from ..hash.hash import checkPassword


private_key = "private_key"


class SessionRepository:
    def createSession(self, email, password) -> str:
        user = UserModel.query.filter_by(email=email).first()
        # user.password != password:
        if not user or not checkPassword(password, user.hashPassword):
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

    def validateSession(self, token):
        token = token.replace("Bearer ", "")

        try:
            payload = decode(token, key=private_key, algorithms=["HS256"])
        except InvalidSignatureError:
            raise AuthError("Invalid Token Signature")
        except ExpiredSignatureError:
            raise AuthError("Expired Token")
        except:
            raise AuthError()
        return payload

    # todo: revalidateSession shall be implemented but is not a priority
    def revalidateSession(self):
        pass
