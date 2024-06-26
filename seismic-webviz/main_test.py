# bokeh serve step_6.py

from bokeh.layouts import column, row
from bokeh.models import Paragraph, Slider, Spinner, Switch, NumericInput, TextInput, RadioButtonGroup
from bokeh.plotting import curdoc
from seismicio import readsu

from widgets.seismic_visualization import SeismicVisualization
from transforms.clip import apply_clip_from_perc
from transforms.gain import do_agc, do_gagc

GAIN_OPTIONS = ["None", "agc", "gagc"]

# Parâmetros de entrada
# ---------------------
file_path = "/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su"
gather_key = "cdp"
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
        gather_key="Offset [m]",
    )
else:
    # Multiple gathers
    seismic_visualization = SeismicVisualization(
        data=sufile.igather[start_igather : start_igather + num_loadedgathers].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )
num_gathers = sufile.num_gathers

current_gather_label = Paragraph(text="Gathers")


def update_information(gather_index_start: int, gather_index_stop: int):
    gather_value_start = sufile.gather_index_to_value(gather_index_start)
    gather_value_end = sufile.gather_index_to_value(gather_index_stop - 1)
    current_gather_label.text = f"Gather {gather_value_start} to {gather_value_end}"
    # simple_paragraph.text = f"Gather WHATERVER"


update_information(start_igather, start_igather + num_loadedgathers)


def apply_gain_single_trace(data, gain_option: str, iwagc, nt: int):
    if gain_option == "agc":
        data = do_agc(data, iwagc, nt)
    elif gain_option == "gagc":
        data = do_gagc(data, iwagc, nt)
    return data


def apply_gain_data(data, gain_option, wagc):
    if gain_option == "None":
        return data
    dt: float = sufile.headers.dt[0] / 1000000.0  # microsseconds to seconds
    nt: int = sufile.num_samples
    iwagc = round(wagc / dt)
    num_traces = data.shape[1]

    for trace_index in range(num_traces):
        trace = data[:, trace_index]
        data[:, trace_index] = apply_gain_single_trace(trace, gain_option, iwagc, nt)

    return data


def update_plotting(igather_start: int, igather_stop: int, perc=None, gain_option=None, wagc_value=0.5):
    # WARNING: this function expects the index or slice to be correct
    print(f"CALL update_plotting({igather_start}, {igather_stop})")

    if igather_start == igather_stop - 1:
        # Single gather

        data = sufile.igather[igather_start].data

        data = apply_gain_data(data, gain_option, wagc_value)

        if perc and perc != 100:
            data = apply_clip_from_perc(data, perc)

        seismic_visualization.update_plot(
            data=data,
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


def _get_igather_slice(start_position_1_based, num_loadedgathers):
    """
    Args:
      position (int): position of the gather, counting started at 1
      num_loadedgathers (int): number of gathers to be loaded

    Returns:
      start_igather (int):
        start index, included endpoint for slicing gathers by index
      stop_igather (int):
        stop index, excluded endpoint for slicing gathers by index
    """
    start_igather = start_position_1_based - 1
    stop_igather = start_igather + num_loadedgathers
    if stop_igather <= num_gathers:
        return (start_igather, stop_igather)
    else:
        return (num_gathers - num_loadedgathers, num_gathers)


def slider_value_callback(attr, old, new):
    print("--------------------------------------")
    print(f"CALL slider_value_callback(new={new})")
    global start_igather, num_loadedgathers, slider
    spinner.disabled = True
    slider.disabled = True

    start_igather = round(new) - 1
    stop_igather = start_igather + num_loadedgathers

    # if exceeding to the right
    if stop_igather > num_gathers:
        start_igather = num_gathers - num_loadedgathers
        stop_igather = num_gathers
        slider.value = start_igather + 1

    update_plotting(start_igather, stop_igather)
    spinner.disabled = False
    slider.disabled = False


def perc_callback(attr, old, new):
    print("PERC CALLBACK")
    perc_value = float(new)
    global start_igather, num_loadedgathers
    update_plotting(start_igather, start_igather + num_loadedgathers, perc=perc_value)


def gain_select_callback(attr, old, new):
    print("gain select CALLBACK")
    global wagc_input
    wagc_value = float(wagc_input.value)
    gain_selection = GAIN_OPTIONS[new]
    perc_value = perc_input.value
    print("agc_value", wagc_value)
    print("gain_select", gain_selection)
    print("perc_value", perc_value)
    # global start_igather, num_loadedgathers
    update_plotting(
        start_igather,
        start_igather + num_loadedgathers,
        perc=perc_value,
        gain_option=gain_selection,
        wagc_value=wagc_value,
    )


def gain_value_callback(attr, old, new):
    print("gain value callback")
    global gain_select_widget
    wagc_value = float(new)
    gain_selection = GAIN_OPTIONS[gain_select_widget.active]
    perc_value = perc_input.value
    print("agc_value", wagc_value)
    print("gain_select", gain_selection)
    print("perc_value", perc_value)
    global start_igather, num_loadedgathers
    update_plotting(
        start_igather,
        start_igather + num_loadedgathers,
        perc=perc_value,
        gain_option=gain_selection,
        wagc_value=wagc_value,
    )


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
    value=start_igather + 1,
    step=1,
    title="Gather sequential number start",
    width=1000,
)
slider.on_change("value_throttled", slider_value_callback)

switch_lines = Switch(active=True)
switch_image = Switch(active=True)
switch_areas = Switch(active=True)
seismic_visualization.assign_line_switch(switch_lines)
seismic_visualization.asssign_image_switch(switch_image)
seismic_visualization.assign_area_switch(switch_areas)

perc_input = NumericInput(value=100, low=1, high=100, title="perc")
perc_input.on_change("value", perc_callback)
gain_select_widget = RadioButtonGroup(labels=GAIN_OPTIONS, active=0)
gain_select_widget.on_change("active", gain_select_callback)
wagc_input = TextInput(value="0.5", title="wagc")
wagc_input.on_change("value", gain_value_callback)

left_tools_column = column(
    current_gather_label,
    row(Paragraph(text="Image"), switch_image),
    row(Paragraph(text="Lines"), switch_lines),
    row(Paragraph(text="Areas"), switch_areas),
    perc_input,
    gain_select_widget,
    wagc_input,
)

bottom_tools_row = row(spinner, slider, sizing_mode="stretch_width")

row_tools_figure = row(children=[left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

curdoc().add_root(column_main)

print(f"Number of gathers: {sufile.num_gathers}\n")
