import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'

type selectedWorkflowsType = Array<IgenericEntitiesType>
type setSelectedWorkflowsType = Dispatch<SetStateAction<selectedWorkflowsType>>
type singleSelectedWorkflowIdType = number | undefined
type setSingleSelectedWorkflowIdType = Dispatch<SetStateAction<singleSelectedWorkflowIdType>>

type useSelectedWorkflowsType = {
  selectedWorkflows: selectedWorkflowsType,
  setSelectedWorkflows: setSelectedWorkflowsType,
  singleSelectedWorkflowId: singleSelectedWorkflowIdType,
  setSingleSelectedWorkflowId: setSingleSelectedWorkflowIdType,
}

interface ISelectedWorkflowsProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISelectedWorkflowsProviderContext {
  selectedWorkflows: selectedWorkflowsType
  setSelectedWorkflows: setSelectedWorkflowsType,
  singleSelectedWorkflowId: singleSelectedWorkflowIdType,
  setSingleSelectedWorkflowId: setSingleSelectedWorkflowIdType,
}

const SelectedWorkflowsProviderContext = createContext<ISelectedWorkflowsProviderContext>({
  selectedWorkflows: [],
  setSelectedWorkflows: () => undefined,
  singleSelectedWorkflowId: undefined,
  setSingleSelectedWorkflowId: () => undefined,
});

export default function SelectedWorkflowsProvider({ children }: ISelectedWorkflowsProviderProps) {
  const [selectedWorkflows, setSelectedWorkflows] = useState<selectedWorkflowsType>([])
  const [singleSelectedWorkflowId, setSingleSelectedWorkflowId] = useState<singleSelectedWorkflowIdType>(undefined)

  return (
    <SelectedWorkflowsProviderContext.Provider
      value={{
        selectedWorkflows,
        setSelectedWorkflows,
        singleSelectedWorkflowId,
        setSingleSelectedWorkflowId
      }}
    >
      {children}
    </SelectedWorkflowsProviderContext.Provider>
  )
}

export function useSelectedWorkflows(): useSelectedWorkflowsType {
  const context = useContext(SelectedWorkflowsProviderContext)
  if (!context)
    throw new Error('useSelectedWorkflows must be used within a SelectedWorkflowsProvider')
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId,
  } = context
  return {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId,
  }
}
