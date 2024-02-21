import { useState, useEffect } from 'react'

import { useDebounce } from 'use-debounce';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';

import DeleteButton from './DeleteButton';
import { getParameters, createNewParameter, updateParameter } from '../services/parameterServices';
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

export default function ParameterForm() {
  const { selectedProgram } = useSelectedProgramCommand()

  const [parameters, setParamenters] = useState<Array<IParameter>>([])
  const [parametersDebounced] = useDebounce(parameters, 2000)

  const updateParameterField = (
    index: number,
    key: "name" | "input_type" | "description",
    newValue: string,
  ) => {
    const newParameters = [...parameters];
    newParameters[index][key] = newValue
    newParameters[index].hasChanges = true
    setParamenters(newParameters)
  }

  useEffect(() => {
    if(!selectedProgram)
      return setParamenters([])
    getParameters(selectedProgram.id).then(programParameters => setParamenters(programParameters))
  }, [selectedProgram])

  useEffect(() => {
    parametersDebounced.forEach((paremeter) => {
      if(paremeter.hasChanges)
        updateParameter(paremeter)
    })
  }, [parametersDebounced])

  return selectedProgram && (
    <>
    <Typography variant="h4">
      Parametros
    </Typography>
    {parameters.map((parameter, index) => (
      <Stack
        direction="row"
        key={index}
        spacing={2}
      >
        <TextField
          label="Nome do Parametro"
          value={parameter.name}
          onChange={(event) => updateParameterField(index, "name", event.target.value)}
        />
        <TextField
          label="Tipo do parametro"
          value={parameter.input_type}
          onChange={(event) => updateParameterField(index, "input_type", event.target.value)}
        />
        <TextField
          label="Descrição do Parametro"
          value={parameter.description}
          onChange={(event) => updateParameterField(index, "description", event.target.value)}
        />
        <DeleteButton
          onClick={() => {
            const newParameters = [...parameters]
            newParameters.splice(index, 1)
            setParamenters(newParameters)
          }}
        />
      </Stack>
    ))}

    <Button
      variant="contained"
      onClick={() => createNewParameter(selectedProgram.id).then(
        (newParameter) => newParameter && setParamenters([...parameters, newParameter])
      )}
    >
      Novo Parametro
    </Button>
    </>
  )
}