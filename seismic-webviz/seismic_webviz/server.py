from .core import Visualization
from bokeh.plotting import curdoc


main = Visualization(
    filename="/storage1/Seismic/dados_teste/marmousi_CDP_stack.su",
)

curdoc().add_root(main.main_model)
