from bokeh.plotting import figure
from bokeh.embed import components

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# create a new plot with a title and axis labels
def getPlot ():
	p = figure(title="Simple lane example", x_axis_label="x", y_axis_label="y")
	p.line(x, y, legend_label="Temp.", line_width=2)

	script, div = components(p)

	return script, div
