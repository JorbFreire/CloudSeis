import type { Dispatch, SetStateAction } from 'react'

import { useLogsStore } from 'store/logsStore'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import GenericDrawer from '../GenericDrawer'

interface IConsoleProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function Console({ isOpen, setIsOpen }: IConsoleProps) {
  const consoleLogs = useLogsStore((state) => state.logs)
  const selectedWorkflowId = useSelectedWorkflowsStore((state) => state.singleSelectedWorkflowId)

  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='bottom'
    >
      <h2>Console</h2>
      {selectedWorkflowId && consoleLogs.get(selectedWorkflowId)?.map((message) => (
        <p key={message}>{message}</p>
      ))}
      <br />
    </GenericDrawer>
  )
}
