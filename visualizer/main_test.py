# bokeh serve step_6.py

from bokeh.layouts import column, layout, row
from bokeh.models import Paragraph, Slider, Switch, RangeSlider
from bokeh.plotting import curdoc, show
from seismicio import readsu

from seismic_visulization import SeismicVisualization

# Parâmetros de entrada
# ---------------------
file_path = "/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su"
gather_key = "cdp"
igather_start = 5
igather_stop = 6

# Ler dado sísmico
# ----------------
sufile = readsu(file_path, gather_key)

# Dados retirados dos headers
# ---------------------------
num_time_samples = sufile.num_samples
interval_time_samples = sufile.headers.dt[0] / 1000000  # µs → s

# SeismicVisualization
# --------------------
seismic_visualization = SeismicVisualization(
    data=sufile.gather[igather_start:igather_stop].data,
    x_positions=None,
    interval_time_samples=interval_time_samples,
)


def range_slider_input_handler(attr, old, new):
    start: int = round(new[0])
    stop: int = round(new[1])
    print(f"igather: {start} {stop}")
    seismic_visualization.update_plot(
        data=sufile.igather[start:stop].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )


# Widgets
# -------
first_gather_index = 0
last_gather_index = sufile.num_gathers - 1

range_slider = RangeSlider(
    start=first_gather_index,
    end=last_gather_index,
    value=(igather_start, igather_stop),
    step=1,
    title="Gather",
)
range_slider.sizing_mode = "stretch_width"
range_slider.on_change("value_throttled", range_slider_input_handler)

switch_lines = Switch(active=True)
switch_image = Switch(active=True)
# switch_areas = Switch(active=True)
seismic_visualization.js_link_lines_visible(switch_lines, "active")
seismic_visualization.js_link_image_visible(switch_image, "active")
# seismic_visualization.js_link_areas_visible(switch_areas, "active")

tools_column = column(
    row(Paragraph(text="Lines"), switch_lines),
    row(Paragraph(text="Image"), switch_image),
    # row(Paragraph(text="Areas"), switch_areas),
)

row_tools_figure = row(children=[tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(children=[row_tools_figure, range_slider], sizing_mode="stretch_both")

curdoc().add_root(column_main)
