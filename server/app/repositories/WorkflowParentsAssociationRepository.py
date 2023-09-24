from ..database.connection import database
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel
from ..errors.AppError import AppError

class WorkflowParentsAssociationRepository:
	def showByWorkflowId(self, id):
		pass

	def create(self, workflowId, parentData):
		parentId = parentData["parentId"]
		parentType = parentData["parentType"]

		if parentType == "lineId":
			line = LineModel.query().filter_by(id=parentId).first()
			if not line:
				raise AppError("Line does not exist", 404)
		elif parentType == "projectId":
			project = ProjectModel.query().filter_by(id=parentId).first()
			if not project:
				raise AppError("Project does not exist", 404)

		newAssociation = WorkflowParentsAssociationModel({
			"workflowId": workflowId,
			parentType: parentId
		})

		database.session.add(newAssociation)
		database.session.commit()

		return newAssociation.getAttributes()
