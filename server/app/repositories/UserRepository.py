from uuid import uuid4, UUID

from ..database.connection import database
from ..models.UserModel import UserModel
from ..errors.AppError import AppError
from ..hash.hash import hashPassword


class UserRepository:
    def showAll(self) -> list[dict]:
        users: list[UserModel] = UserModel.query.all()
        if not users:
            raise AppError("There are no users", 404)

        return [user.getAttributes() for user in users]

    def showById(self, id) -> dict:
        user = UserModel.query.filter_by(id=UUID(id)).first()

        if not user:
            raise AppError("User does not exist", 404)

        return user.getAttributes()

    def create(self, newUserData) -> dict:
        user = UserModel.query.filter_by(email=newUserData["email"]).first()
        if user:
            raise AppError("Email alredy used")
        newId = uuid4()
        hashedPassword = hashPassword(newUserData["password"])
        newUser = UserModel(
            id=newId,
            name=newUserData["name"],
            email=newUserData["email"],
            password=hashedPassword
        )
        database.session.add(newUser)
        database.session.commit()
        return newUser.getAttributes()

    def update(self, id, newUserData) -> dict:
        user = UserModel.query.filter_by(id=UUID(id)).first()
        if not user:
            raise AppError("User does not exist", 404)

        if "name" in newUserData:
            user.name = newUserData["name"]
        if "email" in newUserData:
            user.email = newUserData["email"]

        database.session.commit()
        return user.getAttributes()

    def delete(self, id) -> dict:
        user = UserModel.query.filter_by(id=UUID(id)).first()
        if not user:
            raise AppError("User does not exist", 404)

        database.session.delete(user)
        database.session.commit()
        return user.getAttributes()
