from uuid import uuid4, UUID

from ..database.connection import database
from ..models.UserModel import UserModel
from ..errors.AppError import AppError


class UserRepository:

    def login(self, email, password) -> UserModel:
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            raise AppError("User not found", 404) 
            # Redirect to create route
        if user.password != password:
            raise AppError("Incorrect password", 404)

        return user
    
    def logout(self, id, password) -> UserModel:
        user = UserModel.query.filter_by(id=UUID(id)).first()
        if not user:
            raise AppError("User not found", 404) 

        if user.password != password:
            raise AppError("Incorrect password", 404)

        return user

    def showAll(self):
        users: list[UserModel] = UserModel.query.all()
        if not users:
            raise AppError("There are no users", 404)

        return [user.getAttributes() for user in users]

    def showById(self, id) -> UserModel:
        user = UserModel.query.filter_by(id=UUID(id)).first()

        if not user:
            raise AppError("User does not exist", 404)

        return user.getAttributes()

    def create(self, newUserData):
        user = UserModel.query.filter_by(email=newUserData["email"]).first()
        if user:
            raise AppError("Email alredy used")
        newId = uuid4()
        newUser = UserModel(
            id=newId,
            name=newUserData["name"],
            email=newUserData["email"],
            password=newUserData["password"]
        )
        database.session.add(newUser)
        database.session.commit()
        return newUser.getAttributes()

    def update(self, id, newUserData):
        user = UserModel.query.filter_by(id=UUID(id)).first()
        if not user:
            raise AppError("User does not exist", 404)

        if "name" in newUserData:
            user.name = newUserData["name"]
        if "email" in newUserData:
            user.email = newUserData["email"]

        database.session.commit()
        return user.getAttributes()

    def delete(self, id):
        user = UserModel.query.filter_by(id=UUID(id)).first()
        if not user:
            raise AppError("User does not exist", 404)

        database.session.delete(user)
        database.session.commit()
        return user.getAttributes()
