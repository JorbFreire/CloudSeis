from flask import Blueprint, jsonify

from ..repositories.PlotRepository import PlotRepository

plotRouter = Blueprint("plot-routes", __name__, url_prefix="/get-plot")
plotRepository = PlotRepository()

@plotRouter.route("/<unique_filename>", methods=['GET'])
def showPlotHtmlTags(unique_filename):
    script, div = plotRepository.show(unique_filename)
    return jsonify({
        "script": script,
        "div": div
    })

