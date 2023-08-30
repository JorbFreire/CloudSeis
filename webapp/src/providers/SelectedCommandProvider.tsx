import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'
import { updateCommand } from 'services/commandServices'

type selectedCommandType = ICommand | undefined
type setSelectedCommandType = Dispatch<SetStateAction<selectedCommandType>>

interface ISelectedCommandProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISelectedCommandProviderContext {
  selectedCommand: selectedCommandType
  setSelectedCommand: setSelectedCommandType,
  updateCommandParams: (prop: string) => undefined | void
}

const SelectedCommandProviderContext = createContext<ISelectedCommandProviderContext>({
  selectedCommand: undefined,
  setSelectedCommand: () => undefined,
  updateCommandParams: () => undefined
});

export default function SelectedCommandProvider({ children }: ISelectedCommandProviderProps) {
  const [selectedCommand, setSelectedCommand] = useState<selectedCommandType>([])

  // isso provavelmente vai no unix block provider, 
  // chamando o selecetedCommand de dentro
  // Tem q pensar um pouco mais pra ver a melhor rota

  // Tem q atualizar o update commando no backend também
  const updateCommandParams = (newParameters: string) => {
    if (!selectedCommand)
      return;
    updateCommand(selectedCommand.id, newParameters)
  }

  return (
    <SelectedCommandProviderContext.Provider
      value={{
        selectedCommand,
        setSelectedCommand,
        updateCommandParams
      }}
    >
      {children}
    </SelectedCommandProviderContext.Provider>
  )
}

export function useSelectedCommand(): ISelectedCommandProviderContext {
  const context = useContext(SelectedCommandProviderContext)
  if (!context)
    throw new Error('useSelectedCommand must be used within a SelectedCommandProvider')
  const { selectedCommand, setSelectedCommand, updateCommandParams } = context
  return { selectedCommand, setSelectedCommand, updateCommandParams }
}
