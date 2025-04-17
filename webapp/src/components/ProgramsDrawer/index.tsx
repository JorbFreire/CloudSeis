import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { getGroups } from 'services/programServices'
import { createNewCommand } from 'services/commandServices'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
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
  const singleSelectedWorkflowId = useSelectedWorkflowsStore((state) => state.singleSelectedWorkflowId)
  // *** Commands in the current selected workflow
  const {
    commands,
    setCommands,
    setSelectedCommandId
  } = useCommandsStore((state) => ({
    commands: state.commands,
    setCommands: state.setCommands,
    setSelectedCommandId: state.setSelectedCommandId,
  }))

  // *** Groups of Commands, available commands to insert in the workflow
  const [programsGroups, setProgramsGroups] = useState<Array<IProgramsGroup>>([])

  const addProgramToCurrentWorkflow = (name: string, program_id: number) => {
    if (singleSelectedWorkflowId) {
      createNewCommand(
        singleSelectedWorkflowId,
        program_id,
        name
      ).then((result) => {
        if (!result) return;
        const newCommands = [...commands]
        const posProcessingStaticTabsAmount = 2
        newCommands.splice(newCommands.length - posProcessingStaticTabsAmount, 0, result)
        setCommands(newCommands)

        // *** Turn focous on the new command
        if (typeof result.id !== "number") return
        setSelectedCommandId(result.id)
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
              <button
                onClick={() => addProgramToCurrentWorkflow(
                  program.path_to_executable_file,
                  program.id,
                )}
              >
                Add to queue
              </button>
            </h4>
          ))}
        </div>
      ))}
    </GenericDrawer>
  )
}
