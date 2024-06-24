import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'

type selectedCommandIndexType = number | undefined
type setSelectedCommandIndexType = Dispatch<SetStateAction<number | undefined>>

interface ISelectedCommandIndexProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISelectedCommandIndexProviderContext {
  selectedCommandIndex: selectedCommandIndexType
  setSelectedCommandIndex: setSelectedCommandIndexType
}

const SelectedCommandIndexProviderContext = createContext<ISelectedCommandIndexProviderContext>({
  selectedCommandIndex: undefined,
  setSelectedCommandIndex: () => undefined,
});

export default function SelectedCommandIndexProvider({ children }: ISelectedCommandIndexProviderProps) {
  const [selectedCommandIndex, setSelectedCommandIndex] = useState<selectedCommandIndexType>(undefined)

  return (
    <SelectedCommandIndexProviderContext.Provider
      value={{
        selectedCommandIndex,
        setSelectedCommandIndex,
      }}
    >
      {children}
    </SelectedCommandIndexProviderContext.Provider>
  )
}

export function useSelectedCommandIndex(): ISelectedCommandIndexProviderContext {
  const context = useContext(SelectedCommandIndexProviderContext)
  if (!context)
    throw new Error('useSelectedCommandIndex must be used within a SelectedCommandIndexProvider')
  const {
    selectedCommandIndex,
    setSelectedCommandIndex,
  } = context
  return {
    selectedCommandIndex,
    setSelectedCommandIndex,
  }
}
