from ..database.connection import database
from ..models.SeismicLineModel import SeismicLineModel
from ..models.SeismicWorkflowModel import SeismicWorkflowModel
from ..errors.AppError import AppError

class SeismicWorkflowRepository:
    def showById(self, id):
        workflow = SeismicWorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        return workflow.getAttributes()


    def create(self, seismicLineId, newWorkflowName):
        seismicLine = SeismicLineModel.query.filter_by(id=seismicLineId).first()
        if not seismicLine:
            raise AppError("Seismic Line does not exist", 404)

        newWorkflow = SeismicWorkflowModel(
            seismicLineId=seismicLine.id,
            name=newWorkflowName,
            seismic_file_name=""
        )
        database.session.add(newWorkflow)
        database.session.commit()
        return newWorkflow.getAttributes()

    def updateName(self, id, newWorkflowName):
        pass

    def delete(self, id):
        workflow = SeismicWorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        database.session.delete(workflow)
        database.session.commit()
        return workflow.getAttributes()

