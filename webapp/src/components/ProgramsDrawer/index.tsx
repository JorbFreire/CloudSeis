import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { getGroups } from 'services/programServices'
import { createNewCommand } from 'services/commandServices'
import { useSelectedWorkflows } from 'providers/SelectedWorkflowsProvider'
import { useCommandsStore } from 'store/commandsStore';
import GenericDrawer from "../GenericDrawer"

interface IProgramsDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function ProgramsDrawer({
  isOpen,
  setIsOpen
}: IProgramsDrawerProps) {
  const { singleSelectedWorkflowId } = useSelectedWorkflows()
  // *** Commands in the current selected workflow
  const {
    commands,
    setCommands,
  } = useCommandsStore((state) => ({
    commands: state.commands,
    setCommands: state.setCommands,
  }))

  // *** Groups of Commands, available commands to insert in the workflow
  const [programsGroups, setProgramsGroups] = useState<Array<IProgramsGroup>>([])

  const addProgramToCurrentWorkflow = (name: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    if (singleSelectedWorkflowId) {
      createNewCommand(
        token,
        singleSelectedWorkflowId,
        name
      ).then((result) => {
        if (!result) return;
        const newCommands = [...commands]
        newCommands.push(result)
        setCommands(newCommands)
      })
    }
  }

  useEffect(() => {
    getGroups().then((result) => {
      setProgramsGroups(result)
    })
  }, [])

  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='right'
    >
      <h1>Programs</h1>
      {programsGroups.map((group) => (
        <div
          key={group.id}
        >
          <h2>{group.name}</h2>
          {group.programs.map((program) => (
            <h4
              key={program.id}
            >
              {program.name}
              <button onClick={() => addProgramToCurrentWorkflow(program.name)}>
                Add to queue
              </button>
            </h4>
          ))}
        </div>
      ))}
    </GenericDrawer>
  )
}
