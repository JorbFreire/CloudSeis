import numpy.typing as npt
from bokeh.models import ColumnDataSource, GlyphRenderer, Model, Image
import numpy as np
from bokeh.plotting import figure


class SeismicVisualization:

    def __init__(
            self,
            data: npt.NDArray,
            x_positions: npt.NDArray | None,
            interval_time_samples: float,
            time_unit="s",
            stretch_factor=0.15,
            color="black",
    ):
        # Input checks
        # ------------

        # Input check for stretch_factor
        if not isinstance(stretch_factor, (int, float)):
            raise TypeError("stretch_factor must be a number")

        # Input check for data
        if type(data).__module__ != np.__name__:
            raise TypeError("data must be a numpy array")
        if len(data.shape) != 2:
            raise ValueError("data must be a 2D array")

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        # Input check for x_positions
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        else:
            if type(x_positions).__module__ != np.__name__:
                raise TypeError("x_positions must be a numpy array")
            if len(x_positions.shape) != 1:
                raise ValueError("x_positions must be a 1D array")
            if x_positions.size != num_traces:
                raise ValueError(
                    "The size of x_positions must be equal to the number of "
                    "columns in data, that is, it must be equal to the number "
                    "of traces")

        # Create and set up figure object
        # -------------------------------
        self.plot: figure = figure(
            x_axis_location="above",
            height=800,
            width=1000,
            sizing_mode="stretch_both",
        )

        # Adjust ranges
        self.plot.x_range.range_padding = 0.0
        self.plot.y_range.range_padding = 0.0
        self.plot.y_range.flipped = True

        # Adjust axes
        self.plot.xaxis.axis_label = "Offset (m)"
        if time_unit == "s":
            self.plot.yaxis.axis_label = "Time (s)"
        elif time_unit == "ms":
            self.plot.yaxis.axis_label = "Time (ms)"

        # Create ColumnDataSource objects and add renderers
        # -------------------------------------------------

        # Time sample instants (auxiliary data for all)
        first_time_sample = 0.0
        last_time_sample = first_time_sample + (num_time_samples - 1) * interval_time_samples
        time_sample_instants = np.linspace(
            start=first_time_sample, stop=last_time_sample, num=num_time_samples
        )

        # Create image source
        self.image_source = ColumnDataSource(data={"image": [data]})

        # Auxiliary data for image renderer parameters
        width_x_positions = np.abs(x_positions[0] - x_positions[-1])
        width_time_sample_instants = np.abs(time_sample_instants[0] - time_sample_instants[-1])
        distance_first_x_positions = x_positions[1] - x_positions[0]
        distance_last_x_positions = x_positions[-1] - x_positions[-2]

        # Add image renderer
        self.image_gl: GlyphRenderer = self.plot.image(
            image="image",
            source=self.image_source,
            x=x_positions[0] - distance_first_x_positions / 2,
            y=first_time_sample,
            dw=width_x_positions + (distance_first_x_positions + distance_last_x_positions) / 2,
            dh=width_time_sample_instants,
            palette="Greys256",
            anchor="bottom_left",
            origin="bottom_left",
        )

        # Amplitudes zeros
        amplitudes_zeros = np.zeros(shape=(num_time_samples,))

        # Minimum trace horizontal spacing
        trace_x_spacing = np.min(np.diff(x_positions))

        # Rescale data by trace_x_spacing and stretch_factor
        data_max_std = np.max(np.std(data, axis=0))
        data_rescaled = data / data_max_std * trace_x_spacing * stretch_factor

        xs_list = []
        ys_list = []
        # self.harea_gl_list: list[GlyphRenderer] = []

        for trace_index in range(num_traces):
            x_position = x_positions[trace_index]
            amplitudes = data_rescaled[:, trace_index]

            # fill positive amplitudes
            amplitudes_positive = np.clip(amplitudes, a_min=0, a_max=None)
            # Call harea glyph renderer
            # self.harea_gl_list.append(

            # Add harea renderer
            # self.plot.harea(
            #     x1=amplitudes_zeros + x_position,
            #     x2=amplitudes_positive + x_position,
            #     y=time_sample_instants,
            #     color="black",
            # )
            # )

            # construct CDS for multi_line render
            xs_list.append(amplitudes + x_position)
            ys_list.append(time_sample_instants)

        self.multi_line_source = ColumnDataSource(
            data={
                "xs": xs_list,
                "ys": ys_list,
            }
        )

        # Add multiline renderer
        self.multi_line_gl: GlyphRenderer = self.plot.multi_line(
            xs="xs", ys="ys", source=self.multi_line_source, color=color
        )

    def update_plot(
            self,
            data: npt.NDArray,
            x_positions: npt.NDArray | None,
            interval_time_samples: float,
            time_unit="s",
            stretch_factor=0.15,
            color="black",
    ):
        # Input checks
        # ------------

        # Input check for stretch_factor
        if not isinstance(stretch_factor, (int, float)):
            raise TypeError("stretch_factor must be a number")

        # Input check for data
        if type(data).__module__ != np.__name__:
            raise TypeError("data must be a numpy array")
        if len(data.shape) != 2:
            raise ValueError("data must be a 2D array")

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        # Input check for x_positions
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        else:
            if type(x_positions).__module__ != np.__name__:
                raise TypeError("x_positions must be a numpy array")
            if len(x_positions.shape) != 1:
                raise ValueError("x_positions must be a 1D array")
            if x_positions.size != num_traces:
                raise ValueError(
                    "The size of x_positions must be equal to the number of "
                    "columns in data, that is, it must be equal to the number "
                    "of traces")

        # Update ColumnDataSource objects for renderers
        # ---------------------------------------------

        # Time sample instants
        first_time_sample = 0.0
        last_time_sample = first_time_sample + (num_time_samples - 1) * interval_time_samples
        time_sample_instants = np.linspace(
            start=first_time_sample, stop=last_time_sample, num=num_time_samples
        )

        # Amplitudes zeros
        amplitudes_zeros = np.zeros(shape=(num_time_samples,))

        # Minimum trace horizontal spacing
        trace_x_spacing = np.min(np.diff(x_positions))

        # Rescale data by trace_x_spacing and stretch_factor
        data_max_std = np.max(np.std(data, axis=0))
        data_rescaled = data / data_max_std * trace_x_spacing * stretch_factor

        xs_list = []
        ys_list = []
        # self.harea_gl_list: list[GlyphRenderer] = []
        num_traces = data.shape[1]
        for trace_index in range(num_traces):
            x_position = x_positions[trace_index]
            amplitudes = data_rescaled[:, trace_index]

            # fill positive amplitudes
            amplitudes_positive = np.clip(amplitudes, a_min=0, a_max=None)
            # Add harea renderer
            # self.harea_gl_list.append(
            #     self.plot.harea(
            #         x1=amplitudes_zeros + x_position,
            #         x2=amplitudes_positive + x_position,
            #         y=time_sample_instants,
            #         color="black",
            #     )
            # )

            # construct CDS for line render
            xs_list.append(amplitudes + x_position)
            ys_list.append(time_sample_instants)

        # Update data sources
        # -------------------
        # image
        self.image_source.data = {"image": [data]}
        # multi_line
        self.multi_line_source.data = {"xs": xs_list, "ys": ys_list}

        # Update plot setup
        # -----------------
        # Adjust axes
        self.plot.xaxis.axis_label = "Offset (m)"
        if time_unit == "s":
            self.plot.yaxis.axis_label = "Time (s)"
        elif time_unit == "ms":
            self.plot.yaxis.axis_label = "Time (ms)"

        # Update image renderer's glyph
        # -----------------------------

        width_x_positions = np.abs(x_positions[0] - x_positions[-1])
        width_time_sample_instants = np.abs(time_sample_instants[0] - time_sample_instants[-1])
        distance_first_x_positions = x_positions[1] - x_positions[0]
        distance_last_x_positions = x_positions[-1] - x_positions[-2]

        image_glyph: Image = self.image_gl.glyph
        image_glyph.x = x_positions[0] - distance_first_x_positions / 2
        image_glyph.dw = width_x_positions + (distance_first_x_positions + distance_last_x_positions) / 2
        image_glyph.y = first_time_sample
        image_glyph.dh = width_time_sample_instants

    def js_link_lines_visible(self, model: Model, attr: str):
        """Link a Bokeh model property to the visibility of the wiggle lines"""
        model.js_link(attr, self.multi_line_gl, "visible")

    # def js_link_areas_visible(self, model: Model, attr: str):
    #     """Link a Bokeh model property to the visibility of the wiggle areas"""
    #     for harea_gl in self.harea_gl_list:
    #         model.js_link(attr, harea_gl, "visible")

    def js_link_image_visible(self, model: Model, attr: str):
        """Link a Bokeh model property to the visibility of the image"""
        model.js_link(attr, self.image_gl, "visible")
