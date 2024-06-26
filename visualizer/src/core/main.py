# bokeh serve step_6.py

from bokeh.layouts import column, row
from bokeh.models import Paragraph, Slider, Spinner, Switch
from bokeh.plotting import curdoc
from seismicio import readsu

from src.models.SeismicVisualization import SeismicVisualization

# Parâmetros de entrada
# ---------------------
file_path = "./marmousi_4ms_CS.su"
gather_key = "ep"
num_loadedgathers: int = 1
start_igather: int = 0  # zero-based indexing

# Ler dado sísmico
# ----------------
sufile = readsu(file_path, gather_key)

# Dados retirados dos headers
# ---------------------------
num_time_samples = sufile.num_samples
interval_time_samples = sufile.headers.dt[0] / 1000000  # µs → s

# SeismicVisualization
# --------------------
if num_loadedgathers == 1:
    # Single gather
    seismic_visualization = SeismicVisualization(
        data=sufile.igather[start_igather].data,
        x_positions=sufile.igather[start_igather].headers["offset"],
        interval_time_samples=interval_time_samples,
        gather_key="Offset [m]"
    )
else:
    # Multiple gathers
    seismic_visualization = SeismicVisualization(
        data=sufile.igather[start_igather: start_igather +
                            num_loadedgathers].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )
num_gathers = sufile.num_gathers

simple_paragraph = Paragraph(text="Gathers")


def update_gather_label(gather_index_start: int, gather_index_stop: int):
    gather_value_start = sufile.gather_index_to_value(gather_index_start)
    gather_value_end = sufile.gather_index_to_value(gather_index_stop - 1)
    simple_paragraph.text = f"Gather {gather_value_start} to {gather_value_end}"
    # simple_paragraph.text = f"Gather WHATERVER"


update_gather_label(start_igather, start_igather + num_loadedgathers)


def update_plotting(igather_start: int, igather_stop: int):
    # WARNING: this function expects the index or slice to be correct
    print(f"CALL update_plotting({igather_start}, {igather_stop})")

    if igather_start == igather_stop - 1:
        # Single gather
        seismic_visualization.update_plot(
            data=sufile.igather[igather_start].data,
            x_positions=sufile.igather[igather_start].headers["offset"],
            interval_time_samples=interval_time_samples,
            gather_key="Offset [m]",
        )
    else:
        # Multiple gathers
        seismic_visualization.update_plot(
            data=sufile.igather[igather_start:igather_stop].data,
            x_positions=None,
            interval_time_samples=interval_time_samples,
        )

    update_gather_label(igather_start, igather_stop)


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
    print("--------------------------------------")
    print(f"CALL spinner_value_callback(new={new})")
    global start_igather, num_loadedgathers, spinner
    spinner.disabled = True
    slider.disabled = True

    num_loadedgathers = round(new)

    stop_igather = start_igather + num_loadedgathers
    # if exceeding to the right
    if stop_igather > num_gathers:
        stop_igather = num_gathers
        num_loadedgathers = stop_igather - start_igather + 1
        spinner.value = num_loadedgathers

    update_plotting(start_igather, stop_igather)
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

slider = SliderModel()

switch_lines = Switch(active=True)
switch_image = Switch(active=True)
switch_areas = Switch(active=True)
seismic_visualization.assign_line_switch(switch_lines)
seismic_visualization.assign_image_switch(switch_image)
seismic_visualization.assign_area_switch(switch_areas)

left_tools_column = column(
    simple_paragraph,
    row(Paragraph(text="Image"), switch_image),
    row(Paragraph(text="Lines"), switch_lines),
    row(Paragraph(text="Areas"), switch_areas),
)

bottom_tools_row = row(spinner, slider, sizing_mode="stretch_width")

row_tools_figure = row(children=[
                       left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(
    children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

curdoc().add_root(column_main)

print(f"Number of gathers: {sufile.num_gathers}\n")
