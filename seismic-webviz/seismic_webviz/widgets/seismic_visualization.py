from bokeh.models import Switch

from ..core.SeismicVisualization import SeismicVisualization


def create_seismic_visualization(state: dict, sufile):
    """
    State:
    - [read] num_loadedgathers
    """
    if state["num_loadedgathers"] == 1:
        # Single gather
        seismic_visualization = SeismicVisualization(
            data=sufile.igather[state["gather_index_start"]].data,
            x_positions=sufile.igather[state["gather_index_start"]].headers["offset"],
            interval_time_samples=state["interval_time_samples"],
            gather_key="Offset [m]",
        )
    else:
        # Multiple gathers
        seismic_visualization = SeismicVisualization(
            data=sufile.igather[
                state["gather_index_start"] : state["gather_index_start"] + state["num_loadedgathers"]
            ].data,
            x_positions=None,
            interval_time_samples=state["interval_time_samples"],
        )

    # Toggle visibility
    lines_switch = Switch(active=True)
    image_switch = Switch(active=True)
    areas_switch = Switch(active=True)
    seismic_visualization.assign_line_switch(lines_switch)
    seismic_visualization.assign_image_switch(image_switch)
    seismic_visualization.assign_area_switch(areas_switch)

    return seismic_visualization
