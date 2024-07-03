from seismic_webviz.core import Main
from bokeh.plotting import curdoc


main = Main(
    filename="/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su",
    gather_key="cdp",
)

curdoc().add_root(main.main_model)
