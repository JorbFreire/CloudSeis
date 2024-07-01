import numpy.typing as npt
from transforms.clip import apply_clip_from_perc
from transforms.gain import do_agc, do_gagc
from widgets.gather_label import update_gather_label


def _apply_gain_single_trace(data, gain_option: str, iwagc, nt: int):
    if gain_option == "agc":
        data = do_agc(data, iwagc, nt)
    elif gain_option == "gagc":
        data = do_gagc(data, iwagc, nt)
    return data


def _apply_gain(data: npt.NDArray, gain_option, wagc, sufile) -> npt.NDArray:
    if gain_option == "None":
        return data
    dt: float = sufile.headers.dt[0] / 1000000.0  # microsseconds to seconds
    nt: int = sufile.num_samples
    iwagc = round(wagc / dt)
    num_traces = data.shape[1]

    for trace_index in range(num_traces):
        trace = data[:, trace_index]
        data[:, trace_index] = _apply_gain_single_trace(trace, gain_option, iwagc, nt)

    return data


def _apply_pencentile_clip(data: npt.NDArray, perc: None | int) -> npt.NDArray:
    if (perc is None) or perc == 100:
        return data
    return apply_clip_from_perc(data, perc)


def update_plotting(state: dict, sufile):
    # WARNING: this function expects the index or slice to be correct

    if state["gather_index_start"] == state["gather_index_stop"] - 1:
        # Single gather

        data = sufile.igather[state["gather_index_start"]].data
        data = _apply_gain(data, state["gain_option"], state["wagc_value"], sufile)
        data = _apply_pencentile_clip(data, state["perc"])

        seismic_visualization.update_plot(
            data=data,
            x_positions=sufile.igather[state["gather_index_start"]].headers["offset"],
            interval_time_samples=state["interval_time_samples"],
            gather_key="Offset [m]",
        )
    else:
        # Multiple gathers
        seismic_visualization.update_plot(
            data=sufile.igather[state["gather_index_start"] : state["gather_index_stop"]].data,
            x_positions=None,
            interval_time_samples=state["interval_time_samples"],
        )

    update_gather_label(state, sufile)
