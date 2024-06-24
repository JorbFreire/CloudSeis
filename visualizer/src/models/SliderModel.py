
class SliderModel(Slider):
	__init__():
		start = 1,
		end = sufile.num_gathers,
		value = start_igather + 1,
		step = 1,
		title = "Gather sequential number start",
		width = 1000,
		self.Slider.__init__()

	def slider_value_callback(attr, old, new):
		print("--------------------------------------")
		print(f"CALL slider_value_callback(new={new})")
		global start_igather, num_loadedgathers, slider
		spinner.disabled = True
		slider.disabled = True

		start_igather = round(new) - 1
		stop_igather = start_igather + num_loadedgathers

		# if exceeding to the right
		if stop_igather > num_gathers:
			start_igather = num_gathers - num_loadedgathers
			stop_igather = num_gathers
			slider.value = start_igather + 1

		update_plotting(start_igather, stop_igather)
		spinner.disabled = False
		slider.disabled = False

    on_change=slider_value_callback

# slider.on_change("value_throttled", slider_value_callback)
