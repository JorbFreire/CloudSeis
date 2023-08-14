from bokeh.plotting import figure
from bokeh.embed import components
from seismicio import readsu
import numpy as np

from ..getFilePath import getFilePath

# create a new plot with a title and axis labels
class PlotRepository:
	def show(self, unique_filename):
		file_path = getFilePath(unique_filename)
		suData = readsu(file_path)

		shot_gather = suData.get_shot_gather(100)

		plot = figure()
		plot.x_range.range_padding = 0
		plot.y_range.range_padding = 0

		plot.image(
			image=[shot_gather],
			x=0,
			y=100,
			dw=100,
			dh=100,
			anchor="top_left",
			origin="top_left",
			palesample_positionse="Greys256",
			level="image"
		)

		plot.grid.visible = False

		script, div = components(plot)

		return script, div
	

	def wiggle(self, unique_filename, sample_positions=None, trace_positions=None, color='black', stretch_factor=0.15):
		file_path = getFilePath(unique_filename)
		suData = readsu(file_path)
		traces = suData.traces

		# Input check
		traces, sample_positions, trace_positions, trace_spacing = self._wiggle_input_pre_processing(traces, sample_positions, trace_positions, stretch_factor)    
		number_of_traces = traces.shape[1]

		plot = figure(
			x_range=(trace_positions[0] - trace_spacing, trace_positions[-1] + trace_spacing),
			y_range=(sample_positions[-1], sample_positions[0]),
			x_axis_location='above',
		)

		for trace_index in range(number_of_traces):
			trace = traces[:, trace_index]
			offset = trace_positions[trace_index]
			plot.line(x=trace + offset, y=sample_positions, color=color)

		print("before components(plot)")
		script, div = components(plot)

		print("pre return")
		return script, div
	
	def _wiggle_input_pre_processing(self, data, sample_positions, trace_positions, stretch_factor):
		# Input check for data
		if type(data).__module__ != np.__name__:
			raise TypeError("data must be a numpy array")
		if len(data.shape) != 2:
			raise ValueError("data must be a 2D array")

		# Input check for sample_positions
		if sample_positions is None:
			sample_positions = np.arange(data.shape[0])
		else:
			if type(sample_positions).__module__ != np.__name__:
				raise TypeError("sample_positions must be a numpy array")
			if len(sample_positions.shape) != 1:
				raise ValueError("sample_positions must be a 1D array")
			if sample_positions.shape[0] != data.shape[0]:
				raise ValueError("sample_positions's size must be the equal to to the number of rows in data, "
								"that is, equal to the number of samples")

		# Input check for trace_positions
		if trace_positions is None:
			trace_positions = np.arange(data.shape[1])
		else:
			if type(trace_positions).__module__ != np.__name__:
				raise TypeError("trace_positions must be a numpy array")
			if len(trace_positions.shape) != 1:
				raise ValueError("trace_positions must be a 1D array")
			if trace_positions.shape[0] != data.shape[1]:
				raise ValueError("trace_positions's size must be equal to the number of columns in data, "
								"that is, equal to the number of traces")

		# Input check for stretch factor (sf)
		if not isinstance(stretch_factor, (int, float)):
			raise TypeError("stretch_factor must be a number")

		# Compute trace horizontal spacing
		trace_spacing = np.min(np.diff(trace_positions))

		# Rescale data by trace_spacing and stretch_factor
		data_max_std = np.max(np.std(data, axis=0))
		data = data / data_max_std * trace_spacing * stretch_factor

		return data, sample_positions, trace_positions, trace_spacing
