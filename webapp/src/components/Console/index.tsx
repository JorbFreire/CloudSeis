import type { Dispatch, SetStateAction } from 'react'

import { useConsoleLogs } from 'providers/ConsoleLogsProvider'
import GenericDrawer from '../GenericDrawer'
import { Container } from './styles'

interface IConsoleProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function Console({ isOpen, setIsOpen }: IConsoleProps) {
  const [consoleLogs] = useConsoleLogs()
  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='bottom'
    >
      <Container>
        <h2>Console</h2>
        {consoleLogs && consoleLogs.map((message) => (
          <p>{message}</p>
        ))}
        <br />
      </Container>
    </GenericDrawer>
  )
}
