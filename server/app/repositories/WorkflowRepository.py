from ..database.connection import database
from ..models.LineModel import LineModel
from ..models.WorkflowModel import WorkflowModel
from ..errors.AppError import AppError


class WorkflowRepository:
    def showById(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        return workflow.getAttributes()

    def create(self, lineId, newWorkflowName):
        line = LineModel.query.filter_by(
            id=lineId
        ).first()
        if not line:
            raise AppError("Line does not exist", 404)

        newWorkflow = WorkflowModel(
            lineId=line.id,
            name=newWorkflowName,
            seismic_file_name=""
        )
        database.session.add(newWorkflow)
        database.session.commit()
        return newWorkflow.getAttributes()

    def updateName(self, id, newWorkflowName):
        pass

    def delete(self, id):
        workflow = WorkflowModel.query.filter_by(id=id).first()
        if not workflow:
            raise AppError("Workflow does not exist", 404)

        database.session.delete(workflow)
        database.session.commit()
        return workflow.getAttributes()
