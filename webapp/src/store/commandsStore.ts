import { create } from 'zustand'

import { updateCommand } from 'services/commandServices'
import { getWorkflowByID } from 'services/workflowServices'
import { StaticTabKey } from 'enums/StaticTabKey'

// ! StaticTabKey here looks too much, needs refactoring
type selectedCommandIndexType = number | StaticTabKey | undefined
type commandsType = Array<ICommand>

interface ICommandsStoreState {
  selectedCommandIndex: selectedCommandIndexType
  setSelectedCommandIndex: (newIndex: number) => void
  commands: commandsType
  setCommands: (newValue: commandsType) => void
  loadCommands: (workflowId: number) => void
  selectNewCommand: (newCommand: any) => void
  updateCommandParams: (index: number, newParameters: string) => Promise<void>
}

export const useCommandsStore = create<ICommandsStoreState>((set, get) => ({
  selectedCommandIndex: undefined,
  setSelectedCommandIndex: (newIndex) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    set(() => ({ selectedCommandIndex: newIndex }))
  },
  commands: [],
  setCommands: (newValue) => set(() => ({ commands: [...newValue] })),
  loadCommands: (workflowId) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    getWorkflowByID(token, workflowId)
      .then((result) => {
        if (!result)
          return

        set({ commands: [...result.commands] })
        if (result.commands.length < 1)
          return;
        set({ selectedCommandIndex: result.commands[0].id })
      })
  },
  selectNewCommand: (newCommand) => { return },
  updateCommandParams: async (index: number, newParameters: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    if (!get().commands[index])
      return;
    const updatedCommand = await updateCommand(token, get().commands[index].id, newParameters)
    if (!updatedCommand)
      return
    set((state) => ({
      commands: [...state.commands.map((command, commandIndex) => {
        if (commandIndex == index)
          command.parameters = updatedCommand.parameters
        return command
      })]
    }))
  },
}))
