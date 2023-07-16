from bokeh.plotting import figure
from bokeh.embed import components
from seismicio import readsu

from ..getFilePath import getFilePath

# create a new plot with a title and axis labels
class PlotRepository:
	def show(self, unique_filename):
		file_path = getFilePath(unique_filename)
		suData = readsu(file_path)

		shot_gather = suData.get_shot_gather(100)

		plot = figure()
		plot.x_range.range_padding = 0
		plot.y_range.range_padding = 0

		plot.image(
			image=[shot_gather],
			x=0,
			y=100,
			dw=100,
			dh=100,
			anchor="top_left",
			origin="top_left",
			palette="Greys256",
			level="image"
		)

		plot.grid.visible = False

		script, div = components(plot)

		return script, div
