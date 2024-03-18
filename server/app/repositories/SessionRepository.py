from jwt import encode
from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel


private_key = "private_key"


class SessionRepository:
    def createSession(self, email, password) -> str:
        user = UserModel.query.filter_by(email=email).first()
        if not user or user.password != password:
            raise AuthError("Invalid email or password")

        try:
            token = encode(
                payload=user,
                key=private_key,
                algorithm="HS256"
            )
        except:
            return AuthError("Could not generate token")

        return token

    # revalidateSession shall be implemented but is not a priority
    def revalidateSession(self):
        pass
