from ..database.connection import database
from ..models.UserModel import UserModel

class UserRepository:
    def show(self, id) -> UserModel:
        user = UserModel.query.filter_by(id=id).first()
        return user

    def create(self, newUserData) -> UserModel:
        user = UserModel(newUserData)
        database.session.add(user)
        database.session.commit()
        return user

    def update(self, id, newUserData) -> UserModel:
        user = UserModel.query.filter_by(id=id).first()

        if newUserData.name:
            user.name = newUserData.name
        if newUserData.email:
            user.email = newUserData.email

        database.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        database.session.delete(user)
        database.session.commit()
        pass

