import { useEffect, useState } from "react"
import type { FormEvent } from "react"

import { getParameters } from "services/programServices"
import { updateCommand } from "services/commandServices"

import {
  Container,
  CustomTextField,
  CustomButton,
  CustomTooltip
} from "./styles"

interface ICommandParametersProps {
  command: ICommand | undefined
}

export default function CommandParameters({ command }: ICommandParametersProps) {
  const [availableParameters, setAvailableParameters] = useState<Array<IseismicProgramParameters>>([])
  const [commandParameters, setCommandParameters] = useState<IobjectWithDynamicFields | null>(null)

  const submitParametersUpdate = (event: FormEvent) => {
    event.preventDefault()

    const token = localStorage.getItem("jwt")
    if (!token)
      return
    if (!command)
      return

    updateCommand(token, command.id, JSON.stringify(commandParameters))
  }

  useEffect(() => {
    if (!command)
      return
    getParameters(command.program_id).then(result => {
      setAvailableParameters(result)
    })
    setCommandParameters(JSON.parse(command.parameters))
  }, [command])

  return (
    <Container onSubmit={submitParametersUpdate}>
      {availableParameters.map((parameterField) => (
        <CustomTooltip
          key={parameterField.id}
          title={parameterField.description}
        >
          <CustomTextField
            label={parameterField.name}
            // todo: "type" must be improved to handle complex typing rendering stuff like a select list 
            type={parameterField.input_type}
            required={parameterField.isRequired}

            value={commandParameters ? commandParameters[parameterField.name] : ""}
            onChange={(event) => {
              const temCommandParameters = { ...commandParameters }
              temCommandParameters[parameterField.name] = event.target.value
              setCommandParameters({ ...temCommandParameters })
            }}
            InputLabelProps={{
              shrink: true
            }}
          />
        </CustomTooltip>
      ))}

      <CustomButton
        type="submit"
        variant="contained"
      >
        Save Parameters
      </CustomButton>
    </Container>
  )
}
