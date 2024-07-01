from core.

def gather_index_start_callback(num_loadedgathers, gather_index_start_slider):
    def callback_wrapper(attr, old, new):

        gather_index_start = round(new) - 1
        stop_igather = gather_index_start + num_loadedgathers

        # if exceeding to the right
        if stop_igather > num_gathers:
            gather_index_start = num_gathers - num_loadedgathers
            stop_igather = num_gathers
            gather_index_start_slider.value = gather_index_start + 1

        update_plotting(gather_index_start, stop_igather)

    return callback_wrapper