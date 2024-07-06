import { create } from 'zustand'

import { updateCommand } from 'services/commandServices'
import { getWorkflowByID } from 'services/workflowServices'

type selectedCommandIndexType = number | undefined
type commandsType = Array<ICommand>

interface ILinesStoreState {
  selectedCommandIndex: selectedCommandIndexType
  setSelectedCommandIndex: (newIndex: number) => void
  commands: commandsType
  setCommands: (newValue: commandsType) => void
  loadCommands: (workflowId: number) => void
  selectNewCommand: (newLine: any) => void
  updateCommandParams: (index: number, newParameters: string) => void
}

export const useCommandsStore = create<ILinesStoreState>((set, get) => ({
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
        if (result === 401)
          return

        set({ commands: [...result.commands] })
        if (result.commands.length < 1)
          return;
        set({ selectedCommandIndex: result.commands[0].id })
      })
  },
  selectNewCommand: (newCommand) => { return },
  updateCommandParams: async (index: number, newParameters: string) => {
    if (!get().commands[index])
      return;
    const updatedCommand = await updateCommand(get().commands[index].id, newParameters)
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
