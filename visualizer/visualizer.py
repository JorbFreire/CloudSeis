import numpy as np
from seismicio import readsu
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (
    ColumnDataSource,
    Button,
    TextInput,
    RadioButtonGroup,
    TabPanel,
    Tabs,
    Paragraph,
)
from bokeh.plotting import figure
from wiggle_bokeh import wiggle, get_wiggle_source_xs_ys


def get_shot_gather(shot_index):
    """
    Obtém um shot gather (conjunto de traços que pertencem a um mesmo shot),
    dados os traços e os headers de um arquivo su.

    Traços pertencem ao mesmo shot se eles possuírem o mesmo valor no header ep.

    Args:
        shot_index: Índice do shot gather a ser obtido.

    Returns:
        Shot gather selecionado.
    """
    number_of_traces = traces.shape[1]

    separation_indices = [0]
    ep = headers.ep
    for trace_index in range(1, number_of_traces):
        if ep[trace_index] != ep[trace_index - 1]:
            separation_indices.append(trace_index)

    start_index = separation_indices[shot_index]
    stop_index = separation_indices[shot_index + 1]

    return traces[:, start_index:stop_index]


def update_sources(new_data):
    # Update image view
    image_source.data = {"image": [new_data]}
    # Update wiggle view
    xs_list, ys_list = get_wiggle_source_xs_ys(new_data)
    wiggle_source.data = {"xs": xs_list, "ys": ys_list}


def next_shot():
    global current_shot
    current_shot += 1
    label_current_shot.text = f"Shot gather: {current_shot + 1}"
    new_shot_gather = get_shot_gather(current_shot)
    update_sources(new_shot_gather)


def previous_shot():
    global current_shot
    if current_shot == 0:
        print("Já estamos no primeiro!")
        return
    current_shot -= 1
    label_current_shot.text = f"Shot gather: {current_shot + 1}"
    new_shot_gather = get_shot_gather(current_shot)
    update_sources(new_shot_gather)


def get_perc_trace(trace, perc):
    clip_value = np.percentile(np.abs(trace), perc)
    return np.clip(trace, a_min=-clip_value, a_max=clip_value)


def select_plot_mode_handler():
    if radio_button_group_plot_modes.active == 0:
        print("Wiggle plot")
        global document
    else:
        print("Image plot")


def apply_perc():
    perc = float(perc_input.value)
    print(f"Applying perc {perc}")
    new_shot_gather = get_shot_gather(current_shot)
    print(f"Shape {new_shot_gather.shape}")
    for trace_index in range(new_shot_gather.shape[1]):
        new_shot_gather[:, trace_index] = get_perc_trace(
            new_shot_gather[:, trace_index], perc
        )
    # Update image view
    image_source.data = {"image": [new_shot_gather]}
    # Update wiggle view
    xs_list, ys_list = get_wiggle_source_xs_ys(new_shot_gather)
    wiggle_source.data = {"xs": xs_list, "ys": ys_list}


sudata = readsu("/volume1/Seismic/dados_teste/marmousi_CS.su")
traces = sudata.traces
headers = sudata.headers

number_of_traces = traces.shape[1]

current_shot = 0

# Create Plot object for image view
image_source = ColumnDataSource(data={"image": [get_shot_gather(current_shot)]})
image_plot = figure()
image_plot.x_range.range_padding = image_plot.y_range.range_padding = 0
image_plot.image(
    image="image",
    source=image_source,
    x=0,
    y=0,
    dw=10,
    dh=10,
    palette="Greys256",
    anchor="top_left",
    origin="top_left",
)
# TabPanel for image view
image_tab = TabPanel(child=image_plot, title="Image")

# Plot object for wiggle view
wiggle_plot, wiggle_source = wiggle(get_shot_gather(current_shot))
# TabPanel for wiggle view
wiggle_tab = TabPanel(child=wiggle_plot, title="Wiggle")

button_next_shot = Button(label="Next")
button_next_shot.on_click(next_shot)
button_previous_shot = Button(label="Previous")
button_previous_shot.on_click(previous_shot)
perc_input = TextInput(title="perc", value="90")
button_perc = Button(label="Apply perc")
button_perc.on_click(apply_perc)
# Plot mode selector
PLOT_MODES = ["Wiggle", "Image"]
radio_button_group_plot_modes = RadioButtonGroup(labels=PLOT_MODES, active=0)
radio_button_group_plot_modes.on_event("button_click", select_plot_mode_handler)
label_current_shot = Paragraph(text=f"Shot gather: {current_shot + 1}")

# Set up layouts and add to document
inputs = column(
    label_current_shot, button_next_shot, button_previous_shot, perc_input, button_perc
)
document = curdoc()
document.add_root(row(inputs, Tabs(tabs=[wiggle_tab, image_tab])))
document.title = "Seismic Visualizer"
