from uuid import UUID

from ..database.connection import database
from ..models.SeismicProjectModel import SeismicProjectModel
from ..models.UserModel import UserModel
from ..errors.AppError import AppError

class SeismicProjectRepository:
    def showByUserId(self, userId):
        seismicProjects = SeismicProjectModel.query.filter_by(userId=UUID(userId)).all()
        if not seismicProjects:
            raise AppError("There are no Projects for this user", 404)

        return [seismicProject.getAttributes() for seismicProject in seismicProjects]


    def create(self, userId, newSeismicProjectName: str):
        user = UserModel.query.filter_by(id=UUID(userId)).first()
        if not user:
            raise AppError("User does not exist", 404)

        newSeismicProject = SeismicProjectModel(
            name=newSeismicProjectName,
            userId=user.id
        )
        database.session.add(newSeismicProject)
        database.session.commit()
        return newSeismicProject.getAttributes()


    def updateName(self, projectId, newSeismicProjectName):
        seismicProject = SeismicProjectModel.query.filter_by(id=projectId).first()
        if not seismicProject:
            raise AppError("Project does not exist", 404)
        
        seismicProject.name = newSeismicProjectName
        database.session.commit()
        return seismicProject.getAttributes()


    def delete(self, projectId):
        seismicProject = SeismicProjectModel.query.filter_by(id=projectId).first()
        if not seismicProject:
            raise AppError("Project does not exist", 404)
        
        database.session.delete(seismicProject)
        database.session.commit()
        return seismicProject.getAttributes()

