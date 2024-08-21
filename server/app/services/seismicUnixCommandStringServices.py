import json
from icecream import ic


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
    ic(parameters)
    for parameterKey, parameterValues in parameters.items():
        if not parameterValues:
            continue
        parametersProcessString += f' {parameterKey}='
        parametersProcessString += _getParameter(parameterValues)
    return parametersProcessString


def getSemicUnixCommandString(commandsQueue: list, source_file_path: str, target_file_path: str) -> str:
    # It will generate a string based on filled fields,
    # parameters with empty values (like empty string or empty lists) will be ignored,
    # leting the command line program handle it if not mandatory
    seismicUnixProcessString = ""
    for orderedCommands in commandsQueue:
        for seismicUnixProgram in orderedCommands.getCommands():
            seismicUnixProcessString += f'{seismicUnixProgram["name"]}'
            seismicUnixProcessString += _getAllParameters(
                json.loads((seismicUnixProgram["parameters"]))
            )
            # ! *** *** *** *** *** *** ***
            # todo: it *MUST* be improved when handling multiple commands
            # ! *** *** *** *** *** *** ***
            seismicUnixProcessString += f' < {source_file_path} > {target_file_path}'
    ic(seismicUnixProcessString)
    return seismicUnixProcessString
