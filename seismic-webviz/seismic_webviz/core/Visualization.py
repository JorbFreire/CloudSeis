from . import MultiGatherVisualization, StackVisualization

class Visualization(MultiGatherVisualization, StackVisualization):
	def __init__(self, filename: str, gather_key: str | None = None):
		if gather_key:
			MultiGatherVisualization.__init__(filename, gather_key)
		else:
			StackVisualization.__init__(filename)
