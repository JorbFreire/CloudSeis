import { useEffect, useState } from "react"

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
  const availableParameters: Array<IseismicProgramParameters> = []
  const [commandParameters, setCommandParameters] = useState<IobjectWithDynamicFields | null>(null)

  useEffect(() => command && setCommandParameters(JSON.parse(command.parameters)), [command])
  return (
    <Container>
      {availableParameters.map((parameterField) => (
        <CustomTooltip
          key={parameterField.id}
          title={parameterField.description}
        >
          <CustomTextField
            // todo: "type" must be improved to handle complex typing rendering stuff like a select list 
            type={parameterField.input_type}
            required={parameterField.isRequired}

            value={commandParameters ? commandParameters[parameterField.name] : ""}
            onChange={(event) => {
              const temCommandParameters = { ...commandParameters }
              temCommandParameters[parameterField.name] = event.target.value
              setCommandParameters({ ...temCommandParameters })
            }}
          />
        </CustomTooltip>
      ))}

      <CustomButton>
        Save Parameters
      </CustomButton>
    </Container>
  )
}
