from uuid import UUID

from ..database.connection import database
from ..models.ProjectModel import ProjectModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..models.UserModel import UserModel
from ..errors.AppError import AppError


class ProjectRepository:
    def showByUserId(self, userId):
        projects = ProjectModel.query.filter_by(
            userId=UUID(userId)
        ).all()
        if not projects:
            raise AppError("There are no Projects for this user", 404)

        return [project.getAttributes() for project in projects]

    def create(self, userId, newProjectName: str):
        user = UserModel.query.filter_by(id=UUID(userId)).first()
        if not user:
            raise AppError("User does not exist", 404)

        newProject = ProjectModel(
            name=newProjectName,
            userId=user.id
        )
        database.session.add(newProject)
        database.session.commit()
        return newProject.getAttributes()

    def updateName(self, projectId, newProjectName):
        project = ProjectModel.query.filter_by(
            id=projectId
        ).first()
        if not project:
            raise AppError("Project does not exist", 404)

        project.name = newProjectName
        database.session.commit()
        return project.getAttributes()

    def delete(self, projectId):
        project = ProjectModel.query.filter_by(
            id=projectId
        ).first()
        if not project:
            raise AppError("Project does not exist", 404)

        database.session.delete(project)
        database.session.commit()
        return project.getAttributes()

    # * It does not include workflows inside lines
    def listWorkflowsByProjectId(self, projectId) -> list[dict[str, str]]:
        project = ProjectModel.query.filter_by(
            id=projectId
        ).first()
        if not project:
            raise AppError("Project does not exist", 404)

        workflowParentAssociations = WorkflowParentsAssociationModel.query.filter_by(
            projectId=projectId
        ).all()

        if len(workflowParentAssociations) is 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.id.in_(
                [association.workflowId for association in workflowParentAssociations]
            )
        ).all()

        return [workflow.getResumedAttributes() for workflow in workflows]
