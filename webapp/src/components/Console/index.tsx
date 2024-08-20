import type { Dispatch, SetStateAction } from 'react'

import { useLogsStore } from 'store/logsStore'
import GenericDrawer from '../GenericDrawer'

interface IConsoleProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function Console({ isOpen, setIsOpen }: IConsoleProps) {
  const consoleLogs = useLogsStore((state) => state.logs)
  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='bottom'
    >
      <h2>Console</h2>
      {consoleLogs && consoleLogs.map((message) => (
        <p key={message} >{message}</p>
      ))}
      <br />
    </GenericDrawer>
  )
}
