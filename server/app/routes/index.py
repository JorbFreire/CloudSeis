from flask import Blueprint

from .suFilesRouter import suFileRouter
from .plotRouter import plotRouter
from .userRouter import userRouter

from .seismicProjectRouter import seismicProjectRouter
from .seismicLineRouter import seismicLineRouter
from .seismicWorkflowRouter import seismicWorkflowRouter
from .seismicComandRouter import seismicComandRouter

router = Blueprint("routes", __name__)

# todo: add body data validator for each route
router.register_blueprint(suFileRouter)
router.register_blueprint(plotRouter)
router.register_blueprint(userRouter)

router.register_blueprint(seismicProjectRouter)
router.register_blueprint(seismicLineRouter)
router.register_blueprint(seismicWorkflowRouter)
router.register_blueprint(seismicComandRouter)

