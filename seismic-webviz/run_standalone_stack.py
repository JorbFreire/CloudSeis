from seismic_webviz.core import StackVisualization
from bokeh.plotting import curdoc

main = StackVisualization(
    filename="/storage1/Seismic/dados_teste/marmousi_CDP_stack.su",
)

curdoc().add_root(main.root_layout)
