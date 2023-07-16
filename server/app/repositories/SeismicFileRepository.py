import os
import subprocess
from datetime import datetime
from ..getFilePath import getFilePath

class SeismicFileRepository:
	def _getParameter(parameterValues: list | str | float | int | bool) -> str:
		parameterValuesProcessString = ""
		if not isinstance(parameterValues, list):
			parameterValuesProcessString += f'{parameterValue}'
			return parameterValuesProcessString
		
		for index, parameterValue in enumerate(parameterValues):
			if(index < len(parameterValues) - 1):
				parameterValuesProcessString += f'{parameterValue},'
				continue
			parameterValuesProcessString += f'{parameterValue}'

		return parameterValuesProcessString


	def _getAllParameters(self, parameters) -> str:
		parametersProcessString = ""
		for parameterKey, parameterValues in parameters.items():
			parametersProcessString += f' {parameterKey}='
			parametersProcessString += self._getParameter(parameterValues)
		return parametersProcessString


	def _getSemicUnixCommandString(self, commandsQueue: list, source_file_path: str, changed_file_path: str) -> str:
		seismicUnixProcessString = ""
		for seismicUnixProgram in commandsQueue:
			seismicUnixProcessString += f'{seismicUnixProgram["name"]}' 
			seismicUnixProcessString += self._getAllParameters(seismicUnixProgram["parameters"])
			seismicUnixProcessString += f' < {source_file_path} > {changed_file_path}'
		return seismicUnixProcessString


	def create(self, file) -> str:
		unique_filename = file.filename.replace(".su", "_").replace(" ", "_")
		unique_filename = unique_filename + datetime.now().strftime("%d%m%Y_%H%M%S") + ".su"

		file.save(os.path.join("static", unique_filename))
		return unique_filename


	def update(self, unique_filename, seismicUnixCommandsQueue) -> str:
		source_file_path = getFilePath(unique_filename)
		# todo: dynamically change the name of the file
		changed_file_path = getFilePath(f'2{unique_filename}')
		seismicUnixProcessString = self._getSemicUnixCommandString(seismicUnixCommandsQueue, source_file_path, changed_file_path)
		try:
			process_output = subprocess.check_output(seismicUnixProcessString, shell=True)
			return process_output
		except Exception as error:
			return str(error)