from bokeh.layouts import column, row
from bokeh.models import NumericInput, Paragraph, RadioButtonGroup, Slider, Spinner, Switch, TextInput
from bokeh.plotting import curdoc
from seismicio import readsu
from transforms.clip import apply_clip_from_perc
from transforms.gain import do_agc, do_gagc
from widgets.seismic_visualization import SeismicVisualization

GAIN_OPTIONS = ["None", "agc", "gagc"]


def update_gather_label(gather_index_start: int, gather_index_stop: int):
    gather_value_start = sufile.gather_index_to_value(gather_index_start)
    gather_value_end = sufile.gather_index_to_value(gather_index_stop - 1)
    gather_label.text = f"Gather {gather_value_start} to {gather_value_end}"


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

    update_gather_label(igather_start, igather_stop)


def num_gathers_callback(attr, old, new):
    print("--------------------------------------")
    print(f"CALL spinner_value_callback(new={new})")
    global gather_index_start, num_loadedgathers, num_gathers_spinner
    num_gathers_spinner.disabled = True
    gather_index_start_slider.disabled = True

    num_loadedgathers = round(new)

    stop_igather = gather_index_start + num_loadedgathers
    # if exceeding to the right
    if stop_igather > num_gathers:
        stop_igather = num_gathers
        num_loadedgathers = stop_igather - gather_index_start + 1
        num_gathers_spinner.value = num_loadedgathers

    update_plotting(gather_index_start, stop_igather)
    num_gathers_spinner.disabled = False
    gather_index_start_slider.disabled = False


def gather_index_start_callback(attr, old, new):
    print("--------------------------------------")
    print(f"CALL slider_value_callback(new={new})")
    global gather_index_start, num_loadedgathers, gather_index_start_slider
    num_gathers_spinner.disabled = True
    gather_index_start_slider.disabled = True

    gather_index_start = round(new) - 1
    stop_igather = gather_index_start + num_loadedgathers

    # if exceeding to the right
    if stop_igather > num_gathers:
        gather_index_start = num_gathers - num_loadedgathers
        stop_igather = num_gathers
        gather_index_start_slider.value = gather_index_start + 1

    update_plotting(gather_index_start, stop_igather)
    num_gathers_spinner.disabled = False
    gather_index_start_slider.disabled = False


def perc_callback(attr, old, new):
    print("PERC CALLBACK")
    perc_value = float(new)
    global gather_index_start, num_loadedgathers
    update_plotting(gather_index_start, gather_index_start + num_loadedgathers, perc=perc_value)


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
        gather_index_start,
        gather_index_start + num_loadedgathers,
        perc=perc_value,
        gain_option=gain_selection,
        wagc_value=wagc_value,
    )


def gain_value_callback(attr, old, new):
    print("gain value callback")
    global gain_type_selector
    wagc_value = float(new)
    gain_selection = GAIN_OPTIONS[gain_type_selector.active]
    perc_value = perc_input.value
    print("agc_value", wagc_value)
    print("gain_select", gain_selection)
    print("perc_value", perc_value)
    global gather_index_start, num_loadedgathers
    update_plotting(
        gather_index_start,
        gather_index_start + num_loadedgathers,
        perc=perc_value,
        gain_option=gain_selection,
        wagc_value=wagc_value,
    )


# Parâmetros de entrada
# ---------------------
file_path = "/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su"
gather_key = "cdp"
num_loadedgathers: int = 1
gather_index_start: int = 0  # zero-based indexing

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
        data=sufile.igather[gather_index_start].data,
        x_positions=sufile.igather[gather_index_start].headers["offset"],
        interval_time_samples=interval_time_samples,
        gather_key="Offset [m]",
    )
else:
    # Multiple gathers
    seismic_visualization = SeismicVisualization(
        data=sufile.igather[gather_index_start : gather_index_start + num_loadedgathers].data,
        x_positions=None,
        interval_time_samples=interval_time_samples,
    )
num_gathers = sufile.num_gathers


# Initialize widgets
# ------------------

# Current gather label
gather_label = Paragraph(text="Gathers")
update_gather_label(gather_index_start, gather_index_start + num_loadedgathers)

# Select gather(s) to visualize
gather_index_start_slider = Slider(
    start=1,
    end=sufile.num_gathers,
    value=gather_index_start + 1,
    step=1,
    title="Gather sequential number start",
    width=1000,
)
num_gathers_spinner = Spinner(
    title="Number of gathers to load",
    low=1,
    high=sufile.num_gathers,
    step=1,
    value=num_loadedgathers,
)
gather_index_start_slider.on_change("value_throttled", gather_index_start_callback)
num_gathers_spinner.on_change("value_throttled", num_gathers_callback)

# Toggle visibility
lines_switch = Switch(active=True)
image_switch = Switch(active=True)
areas_switch = Switch(active=True)
seismic_visualization.assign_line_switch(lines_switch)
seismic_visualization.asssign_image_switch(image_switch)
seismic_visualization.assign_area_switch(areas_switch)

# Transform — percentile-based clip
perc_input = NumericInput(value=100, low=1, high=100, title="perc")
perc_input.on_change("value", perc_callback)

# Transform — gain
gain_type_selector = RadioButtonGroup(labels=GAIN_OPTIONS, active=0)
gain_type_selector.on_change("active", gain_select_callback)
wagc_input = TextInput(value="0.5", title="wagc")
wagc_input.on_change("value", gain_value_callback)

# Contruct layout
# ---------------
left_tools_column = column(
    gather_label,
    row(Paragraph(text="Image"), image_switch),
    row(Paragraph(text="Lines"), lines_switch),
    row(Paragraph(text="Areas"), areas_switch),
    perc_input,
    gain_type_selector,
    wagc_input,
)
bottom_tools_row = row(num_gathers_spinner, gather_index_start_slider, sizing_mode="stretch_width")
row_tools_figure = row(children=[left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
column_main = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

curdoc().add_root(column_main)
