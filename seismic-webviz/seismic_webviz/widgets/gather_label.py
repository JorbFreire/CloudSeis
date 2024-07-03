from bokeh.models import Paragraph


# def _update_gather_label(state, sufile, gather_label) -> None:
#     gather_index_start = state["gather_index_start"]
#     gather_index_stop = state["gather_index_start"] + state["num_loadedgathers"]

#     gather_value_start = sufile.gather_index_to_value(gather_index_start)
#     gather_value_end = sufile.gather_index_to_value(gather_index_stop - 1)

#     gather_label.text = f"Gather {gather_value_start} to {gather_value_end}"


# def create_gather_label(sufile) -> Paragraph:

#     gather_label = Paragraph(text="Gathers")
#     _update_gather_label(gather_label)

#     return gather_label


class GatherLabel(Paragraph):

    def update_text(self, state: dict) -> None:
        gather_index_start = state["gather_index_start"]
        gather_index_stop = state["gather_index_start"] + state["num_loadedgathers"]

        gather_value_start = self.sufile.gather_index_to_value(gather_index_start)
        gather_value_end = self.sufile.gather_index_to_value(gather_index_stop - 1)

        self.text = f"Gather {gather_value_start} to {gather_value_end}"

    def __init__(self, sufile):
        self.sufile = sufile
        self.update_text()
