import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'

type selectedCommandType = Array<string> | undefined
type setSelectedCommandType = Dispatch<SetStateAction<selectedCommandType>>

interface ISelectedCommandProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISelectedCommandProviderContext {
  selectedCommand: selectedCommandType
  setSelectedCommand: setSelectedCommandType,
}

const SelectedCommandProviderContext = createContext<ISelectedCommandProviderContext>({
  selectedCommand: [],
  setSelectedCommand: () => undefined,
});

export default function SelectedCommandProvider({ children }: ISelectedCommandProviderProps) {
  const [selectedCommand, setSelectedCommand] = useState<selectedCommandType>([])

  useEffect(() => {

  }, [])

  return (
    <SelectedCommandProviderContext.Provider
      value={{
        selectedCommand,
        setSelectedCommand,
      }}
    >
      {children}
    </SelectedCommandProviderContext.Provider>
  )
}

export function useSelectedCommand(): [selectedCommandType, setSelectedCommandType] {
  const context = useContext(SelectedCommandProviderContext)
  if (!context)
    throw new Error('useSelectedCommand must be used within a SelectedCommandProvider')
  const { selectedCommand, setSelectedCommand } = context
  return [selectedCommand, setSelectedCommand]
}
