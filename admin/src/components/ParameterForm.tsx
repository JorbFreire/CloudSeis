import { useState, useEffect } from 'react'

import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';

import DeleteButton from './DeleteButton';
import { getParameters, createNewParameter } from '../services/parameterServices';
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

export default function ParameterForm() {
  const { selectedProgram } = useSelectedProgramCommand()

  const [parameters, setParamenters] = useState<Array<IParameter>>([])

  useEffect(() => {
    if(!selectedProgram)
      return setParamenters([])
    getParameters(selectedProgram.id).then(programParameters => setParamenters(programParameters))
  }, [selectedProgram])

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
          onChange={(event) => {
            const newParameters = [...parameters];
            newParameters[index].name = event.target.value
            setParamenters(newParameters)
          }}
        />
        <TextField
          label="Tipo do parametro"
          value={parameter.input_type}
          onChange={(event) => {
            const newParameters = [...parameters];
            newParameters[index].input_type = event.target.value
            setParamenters(newParameters)
          }}
        />
        <TextField
          label="Descrição do Parametro"
          value={parameter.description}
          onChange={(event) => {
            const newParameters = [...parameters];
            newParameters[index].description = event.target.value
            setParamenters(newParameters)
          }}
        />
        <DeleteButton onClick={() => {
          const newParameters = [...parameters]
          newParameters.splice(index, 1)
          setParamenters(newParameters)
        }} />
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