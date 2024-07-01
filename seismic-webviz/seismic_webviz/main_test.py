from bokeh.layouts import column, row
from bokeh.models import NumericInput, Paragraph, RadioButtonGroup, Slider, TextInput
from bokeh.plotting import curdoc
from core import get_sufile
from icecream import ic

import widgets

GAIN_OPTIONS = ["None", "agc", "gagc"]


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


state: dict[str, int | float | str | None] = {
    "gather_index_start": 0,  # zero-based indexing
    "num_loadedgathers": 1,
    "perc": 100,
    "gain_option": "None",
    "wagc_value": 0.5,
    "num_gathers": None,
    "interval_time_samples": None,
    "num_time_samples": None,
}

sufile = get_sufile(
    state,
    filename="/storage1/Seismic/dados_teste/marmousi_4ms_CDP.su",
    gather_key="cdp",
)

seismic_visualization = widgets.create_seismic_visualization(state, sufile)

gather_index_start_slider = widgets.create_gather_index_start_slider(state)

num_loadedgathers_spinner = widgets.create_num_loadedgathers_spinner(state)


# Initialize widgets
# ------------------

# gather_index_start_slider =

# Current gather label

# Select starting gather index
# gather_index_start_slider = Slider(
#     start=1,
#     end=sufile.num_gathers,
#     value=gather_index_start + 1,
#     step=1,
#     title="Gather sequential number start",
#     width=1000,
# )
# gather_index_start_slider.on_change(
#     "value_throttled", gather_index_start_callback(num_loadedgathers, gather_index_start_slider)
# )


# Transform — percentile-based clip
# perc_input = NumericInput(value=100, low=1, high=100, title="perc")
# perc_input.on_change("value", perc_callback)

# # Transform — gain
# gain_type_selector = RadioButtonGroup(labels=GAIN_OPTIONS, active=0)
# gain_type_selector.on_change("active", gain_select_callback)
# wagc_input = TextInput(value="0.5", title="wagc")
# wagc_input.on_change("value", gain_value_callback)

# # Contruct layout
# # ---------------
# left_tools_column = column(
#     gather_label,
#     row(Paragraph(text="Image"), image_switch),
#     row(Paragraph(text="Lines"), lines_switch),
#     row(Paragraph(text="Areas"), areas_switch),
#     perc_input,
#     gain_type_selector,
#     wagc_input,
# )
# bottom_tools_row = row(
#     widgets.create_num_gathers_spinner(), gather_index_start_slider, sizing_mode="stretch_width"
# )
# row_tools_figure = row(children=[left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
# main_layout = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

ic(sufile.num_gathers)

# Contruct layout
# ---------------
left_tools_column = column(
    row(Paragraph(text="Image"), seismic_visualization.image_switch),
    row(Paragraph(text="Lines"), seismic_visualization.lines_switch),
    row(Paragraph(text="Areas"), seismic_visualization.areas_switch),
)
bottom_tools_row = row(
    num_loadedgathers_spinner, gather_index_start_slider, sizing_mode="stretch_width"
)
row_tools_figure = row(children=[left_tools_column, seismic_visualization.plot], sizing_mode="stretch_both")
main_layout = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

curdoc().add_root(main_layout)
