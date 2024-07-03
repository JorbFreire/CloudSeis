import numpy.typing as npt
from bokeh.layouts import column, row
from bokeh.models import NumericInput, Paragraph, RadioButtonGroup, Slider, TextInput
from bokeh.plotting import curdoc
from icecream import ic
from seismicio.Models.SuDataModel import SuFile

from seismic_webviz.transforms.gain import do_agc, do_gagc
from seismic_webviz.transforms.clip import apply_clip_from_perc
import seismic_webviz.widgets as widgets

# from widgets import create_gather_index_start_slider, create_seismic_visualization, GatherLabel, create_num_loadedgathers_spinner
from .get_sufile import get_sufile


class Main:

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

    def __init__(self, filename: str, gather_key: str) -> None:
        self.sufile: SuFile = get_sufile(self.state, filename, gather_key)

        self.seismic_visualization = widgets.create_seismic_visualization(self.state, self.sufile)

        self.gather_index_start_slider = widgets.create_gather_index_start_slider(
            self.state, self.update_plotting
        )
        self.num_loadedgathers_spinner = widgets.create_num_loadedgathers_spinner(
            self.state, self.update_plotting
        )

        # self.gather_label = widgets.GatherLabel(self.sufile)

        left_tools_column = column(
            # self.gather_label,
            row(Paragraph(text="Image"), self.seismic_visualization.image_switch),
            row(Paragraph(text="Lines"), self.seismic_visualization.lines_switch),
            row(Paragraph(text="Areas"), self.seismic_visualization.areas_switch),
        )
        bottom_tools_row = row(
            self.num_loadedgathers_spinner, self.gather_index_start_slider, sizing_mode="stretch_width"
        )
        row_tools_figure = row(
            children=[left_tools_column, self.seismic_visualization.plot], sizing_mode="stretch_both"
        )
        self.main_model = column(children=[row_tools_figure, bottom_tools_row], sizing_mode="stretch_both")

    @staticmethod
    def _apply_gain_single_trace(data, gain_option: str, iwagc, nt: int):
        if gain_option == "agc":
            data = do_agc(data, iwagc, nt)
        elif gain_option == "gagc":
            data = do_gagc(data, iwagc, nt)
        return data

    @staticmethod
    def _apply_gain(data: npt.NDArray, gain_option: str, wagc: float, dt: float, nt: int) -> npt.NDArray:
        if gain_option == "None":
            return data
        iwagc = round(wagc / dt)
        num_traces = data.shape[1]

        for trace_index in range(num_traces):
            trace = data[:, trace_index]
            data[:, trace_index] = Main._apply_gain_single_trace(trace, gain_option, iwagc, nt)

        return data

    @staticmethod
    def _apply_pencentile_clip(data: npt.NDArray, perc: None | int) -> npt.NDArray:
        if (perc is None) or perc == 100:
            return data
        return apply_clip_from_perc(data, perc)

    def update_plotting(self):
        # WARNING: this function expects the index or slice to be correct
        print("CALL update_plotting")

        gather_index_stop = self.state["gather_index_start"] + self.state["num_loadedgathers"]

        if self.state["gather_index_start"] == gather_index_stop - 1:
            # Single gather

            data = self.sufile.igather[self.state["gather_index_start"]].data
            data = self._apply_gain(
                data,
                gain_option=self.state["gain_option"],
                wagc=self.state["wagc_value"],
                dt=self.state["interval_time_samples"],
                nt=self.state["num_time_samples"],
            )
            data = self._apply_pencentile_clip(data, self.state["perc"])

            self.seismic_visualization.update_plot(
                data=data,
                x_positions=self.sufile.igather[self.state["gather_index_start"]].headers["offset"],
                interval_time_samples=self.state["interval_time_samples"],
                gather_key="Offset [m]",
            )
        else:
            # Multiple gathers
            self.seismic_visualization.update_plot(
                data=self.sufile.igather[self.state["gather_index_start"] : gather_index_stop].data,
                x_positions=None,
                interval_time_samples=self.state["interval_time_samples"],
            )

        # update_gather_label()
