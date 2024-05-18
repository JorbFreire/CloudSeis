# bokeh serve step_6.py

from bokeh.layouts import column, row
from bokeh.models import Paragraph, RangeSlider, Switch
from bokeh.plotting import curdoc
from seismicio import readsu

from seismic_visualization import SeismicVisualization

# Parâmetros de entrada
# ---------------------
file_path = "/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su"
gather_key = "cdp"
igather_start = 10
igather_stop = 12

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
    end=last_gather_index + 1,  # because igather slicing is not inclusive at stop
    value=(igather_start, igather_stop),
    step=1,
    title="Gather",
)
range_slider.sizing_mode = "stretch_width"
range_slider.on_change("value_throttled", range_slider_input_handler)

switch_lines = Switch(active=True)
switch_image = Switch(active=True)
switch_areas = Switch(active=True)
seismic_visualization.assign_line_switch(switch_lines)
seismic_visualization.js_link_image_visible(switch_image, "active")
seismic_visualization.assign_harea_switch(switch_areas)

tools_column = column(
    row(Paragraph(text="Image"), switch_image),
    row(Paragraph(text="Lines"), switch_lines),
    row(Paragraph(text="Areas"), switch_areas),
)

row_tools_figure = row(children=[tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(children=[row_tools_figure, range_slider], sizing_mode="stretch_both")

curdoc().add_root(column_main)
