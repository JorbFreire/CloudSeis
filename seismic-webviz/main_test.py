# bokeh serve step_6.py

from bokeh.layouts import column, row
from bokeh.models import Paragraph, Slider, Spinner, Switch
from bokeh.plotting import curdoc
from seismicio import readsu

from seismic_visualization import SeismicVisualization

# Parâmetros de entrada
# ---------------------
file_path = "/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su"
gather_key = "cdp"
num_loadedgathers: int = 2
start_loadedgathers: int = 0  # zero-based indexing

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
    data=sufile.igather[start_loadedgathers : start_loadedgathers + num_loadedgathers].data,
    x_positions=None,
    interval_time_samples=interval_time_samples,
)
num_gathers = sufile.num_gathers

simple_paragraph = Paragraph(text="Gathers")


def update_information(gather_index_start: int, gather_index_stop: int):
    gather_value_start = sufile.gather_index_to_value(gather_index_start)
    gather_value_end = sufile.gather_index_to_value(gather_index_stop)
    simple_paragraph.text = f"Gather {gather_value_start} to {gather_value_end}"


update_information(start_loadedgathers, start_loadedgathers + num_loadedgathers)


def update_plotting(igather_start: int, igather_stop: int):
    # This function expects the index or slice to be correct
    print(f"PLOT igather[{igather_start}:{igather_stop}]")
    seismic_visualization.update_plot(
        data=sufile.igather[igather_start:igather_stop].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )
    update_information(igather_start, igather_stop)


def range_slider_input_handler(attr, old, new):
    start: int = round(new[0])
    stop: int = round(new[1])
    print(f"igather: {start} {stop}")
    seismic_visualization.update_plot(
        data=sufile.igather[start:stop].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )


def spinner_value_callback(attr, old, new):
    global start_loadedgathers, num_loadedgathers, spinner
    spinner.disabled = True
    slider.disabled = True

    num_loadedgathers = round(new)

    stop_loadedgathers = start_loadedgathers + num_loadedgathers
    # if exceeding to the right
    if stop_loadedgathers > num_gathers:
        stop_loadedgathers = num_gathers
        num_loadedgathers = stop_loadedgathers - start_loadedgathers + 1
        spinner.value = num_loadedgathers

    update_plotting(start_loadedgathers, stop_loadedgathers)
    spinner.disabled = False
    slider.disabled = False


def slider_value_callback(attr, old, new):
    global start_loadedgathers, num_loadedgathers, slider
    spinner.disabled = True
    slider.disabled = True
    start_loadedgathers = round(new) - 1
    stop_loadedgathers = start_loadedgathers + num_loadedgathers
    # if exceeding to the right
    if stop_loadedgathers > num_gathers:
        start_loadedgathers = num_gathers - num_loadedgathers
        stop_loadedgathers = num_gathers
        slider.value = start_loadedgathers

    update_plotting(start_loadedgathers, stop_loadedgathers)
    spinner.disabled = False
    slider.disabled = False


# Widgets
# -------
first_gather_index = 0
last_gather_index = sufile.num_gathers - 1

spinner = Spinner(
    title="Number of gathers to load",
    low=1,
    high=sufile.num_gathers,
    step=1,
    value=num_loadedgathers,
)
spinner.on_change("value_throttled", spinner_value_callback)

slider = Slider(
    start=1,
    end=sufile.num_gathers,
    value=start_loadedgathers + 1,
    step=1,
    title="Gather sequential number start",
    sizing_mode="stretch_width",
)
slider.on_change("value_throttled", slider_value_callback)

switch_lines = Switch(active=True)
switch_image = Switch(active=True)
switch_areas = Switch(active=True)
seismic_visualization.assign_line_widget(switch_lines)
seismic_visualization.asssign_image_widget(switch_image)
seismic_visualization.assign_area_widget(switch_areas)

left_tools_column = column(
    simple_paragraph,
    row(Paragraph(text="Image"), switch_image),
    row(Paragraph(text="Lines"), switch_lines),
    row(Paragraph(text="Areas"), switch_areas),
)

bottom_tools_row = row(spinner, slider, sizing_mode="stretch_width")

row_tools_figure = row(children=[left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

curdoc().add_root(column_main)
