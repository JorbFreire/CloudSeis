import subprocess
from .getFilePath import getFilePath

def getSemicUnixCommandString(commandsQueue: list, source_file_path: str, changed_file_path: str) -> str:
	def getParameter(parameterValues: list | str | float | int | bool) -> str:
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


	def getAllParameters(parameters) -> str:
		parametersProcessString = ""

		for parameterKey, parameterValues in parameters.items():
			parametersProcessString += f' {parameterKey}='
			parametersProcessString += getParameter(parameterValues)

		return parametersProcessString


	seismicUnixProcessString = ""

	for seismicUnixProgram in commandsQueue:
		seismicUnixProcessString += f'{seismicUnixProgram["name"]}' 
		seismicUnixProcessString += getAllParameters(seismicUnixProgram["parameters"])
		seismicUnixProcessString += f' < {source_file_path} > {changed_file_path}'
		
	return seismicUnixProcessString



def runSeismicUnix(unique_filename, seismicUnixCommandsQueue):
	source_file_path = getFilePath(unique_filename)
	# todo: change the name of the file
	changed_file_path = getFilePath(f'2{unique_filename}')

	seismicUnixProcessString = getSemicUnixCommandString(seismicUnixCommandsQueue, source_file_path, changed_file_path)


	# "sufilter f=10,20,150,200 amps=1,1,0,0 <data_to_be_filtered.su >low_pass_data.su"
	try:
		process_output = subprocess.check_output(seismicUnixProcessString, shell=True)
	except Exception as error:
		return str(error)
