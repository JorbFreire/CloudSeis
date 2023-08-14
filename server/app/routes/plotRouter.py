from flask import Blueprint, jsonify
from time import time

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


@plotRouter.route("/wiggle/<unique_filename>", methods=['GET'])
def showWigglePlotHtmlTags(unique_filename):
    print("showWigglePlotHtmlTags")
    start = time()
    script, div = plotRepository.wiggle(unique_filename)
    end = time()
    print(div)
    print(end - start)
    return jsonify({
        "script": script,
        "div": div
    })

