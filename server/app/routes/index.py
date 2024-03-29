from flask import Blueprint

from .suFilesRouter import suFileRouter
from .userRouter import userRouter

from .projectRouter import projectRouter
from .lineRouter import lineRouter
from .workflowRouter import workflowRouter
from .commandRouter import commandRouter

from .datasetRouter import datasetRouter

from .programRouter import programRouter
from .programGroupRouter import programGroupRouter
from .parameterRouter import parameterRouter

router = Blueprint("routes", __name__)

# todo: add body data validator for each route
router.register_blueprint(suFileRouter)
router.register_blueprint(userRouter)

router.register_blueprint(projectRouter)
router.register_blueprint(lineRouter)
router.register_blueprint(workflowRouter)
router.register_blueprint(commandRouter)

router.register_blueprint(datasetRouter)

router.register_blueprint(programRouter)
router.register_blueprint(programGroupRouter)
router.register_blueprint(parameterRouter)
