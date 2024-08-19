import json


def _getParameter(parameterValues: list | str | float | int | bool) -> str:
    parameterValuesProcessString = ""
    if not isinstance(parameterValues, list):
        parameterValuesProcessString += f'{parameterValues}'
        return parameterValuesProcessString

    for index, parameterValue in enumerate(parameterValues):
        if index < len(parameterValues) - 1:
            parameterValuesProcessString += f'{parameterValue},'
            continue
        parameterValuesProcessString += f'{parameterValue}'

    return parameterValuesProcessString


def _getAllParameters(parameters) -> str:
    parametersProcessString = ""
    for parameterKey, parameterValues in parameters.items():
        if not parameterValues:
            continue
        parametersProcessString += f' {parameterKey}='
        parametersProcessString += _getParameter(parameterValues)
    return parametersProcessString


def getSemicUnixCommandString(commandsQueue: list, source_file_path: str, target_file_path: str) -> str:
    seismicUnixProcessString = ""
    for orderedCommands in commandsQueue:
        for seismicUnixProgram in orderedCommands.getCommands():
            seismicUnixProcessString += f'{seismicUnixProgram["name"]}'
            seismicUnixProcessString += _getAllParameters(
                json.loads((seismicUnixProgram["parameters"]))
            )
            seismicUnixProcessString += f' < {source_file_path} > {target_file_path}'
    return seismicUnixProcessString
