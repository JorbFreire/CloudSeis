from jwt import encode
from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel
from ..hash.hash import checkPassword


private_key = "private_key"


class SessionRepository:
    def createSession(self, email, password) -> str:
        user = UserModel.query.filter_by(email=email).first()
        if not user or not checkPassword(password, user.hashPassword): #user.password != password:
            raise AuthError("Invalid email or password")

        try:
            token = encode(
                payload=user.getAttributes(),
                key=private_key,
                algorithm="HS256"
            )
        except:
            raise AuthError("Could not generate token")

        return token

    # todo: revalidateSession shall be implemented but is not a priority
    def revalidateSession(self):
        pass
