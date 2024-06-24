import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'
import { updateCommand } from 'services/commandServices'

type commandsType = Array<ICommand>
type setCommandsType = Dispatch<SetStateAction<commandsType>>

interface ICommandsProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ICommandsProviderContext {
  commands: commandsType
  setCommands: setCommandsType
  updateCommandParams: (index: number, newParameters: string) => void
}

const CommandsProviderContext = createContext<ICommandsProviderContext>({
  commands: [],
  setCommands: () => [],
  updateCommandParams: () => undefined,
});

export default function CommandsProvider({ children }: ICommandsProviderProps) {
  const [commands, setCommands] = useState<commandsType>([])

  const updateCommandParams = (index: number, newParameters: string) => {
    if (!commands[index])
      return;
    updateCommand(commands[index].id, newParameters)
  }

  return (
    <CommandsProviderContext.Provider
      value={{
        commands,
        setCommands,
        updateCommandParams,
      }}
    >
      {children}
    </CommandsProviderContext.Provider>
  )
}

export function useCommands(): ICommandsProviderContext {
  const context = useContext(CommandsProviderContext)
  if (!context)
    throw new Error('useCommands must be used within a CommandsProvider')
  const {
    commands,
    setCommands,
    updateCommandParams,
  } = context
  return {
    commands,
    setCommands,
    updateCommandParams,
  }
}
