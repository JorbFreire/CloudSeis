import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.ranges import DataRange1d


def wiggle(
    data,
    time_sample_positions=None,
    x_positions=None,
    color="black",
    stretch_factor=0.15,
):
    # Input check for data
    if type(data).__module__ != np.__name__:
        raise TypeError("data must be a numpy array")
    if len(data.shape) != 2:
        raise ValueError("data must be a 2D array")

    # Input check for time_sample_positions
    if time_sample_positions is None:
        time_sample_positions = np.arange(data.shape[0])
    else:
        if type(time_sample_positions).__module__ != np.__name__:
            raise TypeError("time_sample_positions must be a numpy array")
        if len(time_sample_positions.shape) != 1:
            raise ValueError("time_sample_positions must be a 1D array")
        if time_sample_positions.shape[0] != data.shape[0]:
            raise ValueError(
                "time_sample_positions size must be the equal to to the number of rows in data, "
                "that is, equal to the number of samples"
            )

    # Input check for x_positions
    if x_positions is None:
        x_positions = np.arange(data.shape[1])
    else:
        if type(x_positions).__module__ != np.__name__:
            raise TypeError("x_positions must be a numpy array")
        if len(x_positions.shape) != 1:
            raise ValueError("x_positions must be a 1D array")
        if x_positions.shape[0] != data.shape[1]:
            raise ValueError(
                "x_positions size must be equal to the number of columns in data, "
                "that is, equal to the number of traces"
            )

    # Input check for stretch factor (sf)
    if not isinstance(stretch_factor, (int, float)):
        raise TypeError("stretch_factor must be a number")

    # Compute trace horizontal spacing
    trace_x_spacing = np.min(np.diff(x_positions))

    # Rescale data by trace_x_spacing and stretch_factor
    data_max_std = np.max(np.std(data, axis=0))
    data = data / data_max_std * trace_x_spacing * stretch_factor

    # Create Plot instance
    plot = figure(x_axis_location="above")
    plot.x_range = DataRange1d(
        start=x_positions[0] - trace_x_spacing,
        end=x_positions[-1] + trace_x_spacing,
    )
    plot.y_range = DataRange1d(
        start=time_sample_positions[-1],
        end=time_sample_positions[0],
    )

    number_of_traces = data.shape[1]

    xs_list = []
    ys_list = []
    for trace_index in range(number_of_traces):
        trace = data[:, trace_index]
        offset = x_positions[trace_index]
        xs_list.append(trace + offset)
        ys_list.append(time_sample_positions)

    source = ColumnDataSource(
        data={
            "xs": xs_list,
            "ys": ys_list,
        }
    )

    # Use multiline glyph renderer
    plot.multi_line(xs="xs", ys="ys", source=source, color=color)

    return plot, source


def get_wiggle_source_xs_ys(
    data,
    time_sample_positions=None,
    x_positions=None,
    stretch_factor=0.15,
):
    # Input check for data
    if type(data).__module__ != np.__name__:
        raise TypeError("data must be a numpy array")
    if len(data.shape) != 2:
        raise ValueError("data must be a 2D array")

    # Input check for time_sample_positions
    if time_sample_positions is None:
        time_sample_positions = np.arange(data.shape[0])
    else:
        if type(time_sample_positions).__module__ != np.__name__:
            raise TypeError("time_sample_positions must be a numpy array")
        if len(time_sample_positions.shape) != 1:
            raise ValueError("time_sample_positions must be a 1D array")
        if time_sample_positions.shape[0] != data.shape[0]:
            raise ValueError(
                "time_sample_positions size must be the equal to to the number of rows in data, "
                "that is, equal to the number of samples"
            )

    # Input check for x_positions
    if x_positions is None:
        x_positions = np.arange(data.shape[1])
    else:
        if type(x_positions).__module__ != np.__name__:
            raise TypeError("x_positions must be a numpy array")
        if len(x_positions.shape) != 1:
            raise ValueError("x_positions must be a 1D array")
        if x_positions.shape[0] != data.shape[1]:
            raise ValueError(
                "x_positions size must be equal to the number of columns in data, "
                "that is, equal to the number of traces"
            )

    # Input check for stretch factor (sf)
    if not isinstance(stretch_factor, (int, float)):
        raise TypeError("stretch_factor must be a number")

    # Compute trace horizontal spacing
    trace_x_spacing = np.min(np.diff(x_positions))

    # Rescale data by trace_x_spacing and stretch_factor
    data_max_std = np.max(np.std(data, axis=0))
    data = data / data_max_std * trace_x_spacing * stretch_factor

    number_of_traces = data.shape[1]
    xs_list = []
    ys_list = []
    for trace_index in range(number_of_traces):
        trace = data[:, trace_index]
        offset = x_positions[trace_index]
        xs_list.append(trace + offset)
        ys_list.append(time_sample_positions)

    return xs_list, ys_list
