from ..database.connection import database
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel
from ..models.DataSetModel import DataSetModel
from ..errors.AppError import AppError


class WorkflowParentsAssociationRepository:
    def showByWorkflowId(self, id):
        pass

    def create(self, workflowId, parentData):
        parentId = parentData["parentId"]
        parentTypeKey = parentData["parentType"]

        if parentTypeKey == "lineId":
            line = LineModel.query.filter_by(id=parentId).first()
            if not line:
                raise AppError("Line does not exist", 404)
        elif parentTypeKey == "projectId":
            project = ProjectModel.query.filter_by(id=parentId).first()
            if not project:
                raise AppError("Project does not exist", 404)
        elif parentTypeKey == "datasetId":
            dataset = DataSetModel.query.filter_by(id=parentId).first()
            if not dataset:
                raise AppError("Dataset does not exist", 404)

        # * The "parentTypeKey" is a dynamic key for this association table
        # * once it will have just two of the three possible collumns filled
        newAssociationParameterDict = {
            "workflowId": workflowId,
            parentTypeKey: parentId
        }
        newAssociation = WorkflowParentsAssociationModel(
            # * This "**" operator unpacks the dictionary, so it can be used
            # * as the constructor parameter
            **newAssociationParameterDict
        )

        database.session.add(newAssociation)
        database.session.commit()

        return newAssociation.getAttributes()

    # def delete(self, workflowId):
    #     workflow = WorkflowParentsAssociationModel.query.filter_by(workflowId=workflowId).first()
    #     if not workflow:
    #         raise AppError("Workflow does not exist", 404)
    #     database.session.delete(workflow)
    #     database.session.commit()
