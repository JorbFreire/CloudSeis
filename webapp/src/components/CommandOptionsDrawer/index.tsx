import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { useSelectedCommand } from 'providers/SelectedCommandProvider';
import GenericDrawer from "../GenericDrawer"
import { useDebouncedCallback } from 'use-debounce';

interface ICommandOptionsDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function CommandOptionsDrawer({
  isOpen,
  setIsOpen
}: ICommandOptionsDrawerProps) {
  const { selectedCommand, updateCommandParams } = useSelectedCommand()
  const [parameters, setParameters] = useState<any>([])

  const parametersUpdateDebounced = useDebouncedCallback(() => {
    updateCommandParams(JSON.stringify(parameters))
  }, 4000)

  const updateInput = (value: string, parameterKey: string | unknown) => {
    if (typeof parameterKey !== 'string') return;

    const newParameters = { ...parameters }
    newParameters[parameterKey] = value
    setParameters(newParameters)

    parametersUpdateDebounced()
  }

  useEffect(() => {
    if (selectedCommand?.parameters)
      setParameters(JSON.parse(selectedCommand.parameters))
  }, [selectedCommand])

  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='right'
    >
      <h1>Command</h1>
      {Object.entries(parameters).map((key, parameter: any) => (
        <input
          type="text"
          placeholder={parameter.name}
          value={parameter.value}
          onChange={(event) => updateInput(event.target.value, key)}
        />
      ))}
    </GenericDrawer>
  )
}
