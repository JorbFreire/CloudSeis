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
  setSelectedCommand: setSelectedCommandType
  updateCommandParams: (newParameters: string) => undefined | void
  // "suFileName" is kept here as an workarround and shall be better placed soon
  suFileName: string
  setSuFileName: (newSuFileName: string) => undefined | void
}

const SelectedCommandProviderContext = createContext<ISelectedCommandProviderContext>({
  selectedCommand: undefined,
  setSelectedCommand: () => undefined,
  updateCommandParams: () => undefined,
  // "suFileName" is kept here as an workarround and shall be better placed soon
  suFileName: "",
  setSuFileName: () => undefined,
});

export default function SelectedCommandProvider({ children }: ISelectedCommandProviderProps) {
  const [selectedCommand, setSelectedCommand] = useState<selectedCommandType>(undefined)
  // "suFileName" is kept here as an workarround and shall be better placed soon
  const [suFileName, setSuFileName] = useState("")

  // isso provavelmente vai no unix block provider, 
  // chamando o selecetedCommand de dentro
  // Tem q pensar um pouco mais pra ver a melhor rota

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
        updateCommandParams,
        // "suFileName" is kept here as an workarround and shall be better placed soon
        suFileName,
        setSuFileName,
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
  const {
    selectedCommand,
    setSelectedCommand,
    updateCommandParams,
    // "suFileName" is kept here as an workarround and shall be better placed soon
    suFileName,
    setSuFileName,
  } = context
  return {
    selectedCommand,
    setSelectedCommand,
    updateCommandParams,
    // "suFileName" is kept here as an workarround and shall be better placed soon
    suFileName,
    setSuFileName,
  }
}
