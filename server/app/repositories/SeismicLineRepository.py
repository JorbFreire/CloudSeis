from ..database.connection import database
from ..models.SeismicProjectModel import SeismicProjectModel
from ..models.SeismicLineModel import SeismicLineModel
from ..errors.AppError import AppError

class SeismicLineRepository:
    def showBySeismicProjectId(self, seismicProjectId):
        seismicLines = SeismicLineModel.query.filter_by(
            seismicProjectId=seismicProjectId
        ).all()
        if not seismicLines:
            raise AppError("There are no Lines for this user", 404)

        return [seismicLine.getAttributes() for seismicLine in seismicLines]


    def create(self, seismicProjectId, newSeismicLineName):
        seismicProject = SeismicProjectModel.query.filter_by(id=seismicProjectId).first()
        if not seismicProject:
            raise AppError("Seismic Project does not exist", 404)

        newSeismicLine = SeismicLineModel(
            name=newSeismicLineName,
            seismicProjectId=seismicProject.id
        )
        database.session.add(newSeismicLine)
        database.session.commit()
        return newSeismicLine.getAttributes()


    def update(self, id, newSeismicLineData):
        pass


    def delete(self, id):
        seismicLine = SeismicLineModel.query.filter_by(id=id).first()
        if not seismicLine:
            raise AppError("Line does not exist", 404)

        database.session.delete(seismicLine)
        database.session.commit()
        return seismicLine.getAttributes()

