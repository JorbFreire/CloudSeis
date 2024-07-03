from bokeh.models import Spinner
from icecream import ic


def create_num_loadedgathers_spinner(state: dict, update_func) -> Spinner:
    """
    State
    - [read] num_gathers, gather_index_start
    - [read, write] num_loadedgathers
    """
    num_loadedgathers_spinner = Spinner(
        title="Number of gathers to load",
        low=1,
        # high=state["num_gathers"],
        step=1,
        value=state["num_loadedgathers"],
    )

    def callback(attr: str, old, new):
        print(f"\nCALLBACK num_loadedgathers. new={new}")

        num_loadedgathers: int = round(new)

        # if exceeding to the right
        gather_index_stop = state["gather_index_start"] + num_loadedgathers
        if gather_index_stop > state["num_gathers"]:
            ic("EXCEEDED")
            num_loadedgathers_spinner.value = state["num_gathers"] - state["gather_index_start"]
            return

        state["num_loadedgathers"] = num_loadedgathers
        ic(state)
        update_func()

    num_loadedgathers_spinner.on_change("value_throttled", callback)

    return num_loadedgathers_spinner
