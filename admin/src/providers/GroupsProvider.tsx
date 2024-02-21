import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { getGroups, createNewGroup, deleteGroup } from '../services/programGroupServices'

interface IGroupsProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface IGroupsContext {
  programGroups: Array<IProgramsGroup>
  createProgramGroup: (newGroupData: IProgramsGroupConstructor) => undefined | void
  deleteProgramGroup: (groupId: number) => undefined | void
}

const GroupsContext = createContext<IGroupsContext>({
  programGroups: [],
  createProgramGroup: () => undefined,
  deleteProgramGroup: () => undefined,
});

export default function GroupsProvider({ children }: IGroupsProviderProps) {
  const [programGroups, setProgramGroups] = useState< Array<IProgramsGroup> >([])

  const createProgramGroup = (newGroupData: IProgramsGroupConstructor) => {
    createNewGroup(newGroupData).then(newGroup => newGroup && setProgramGroups([...programGroups, newGroup]))
  }

  const deleteProgramGroup = (groupId: number) => {
    deleteGroup(groupId).then((responseData) => {
      if(responseData) {
        const newProgramGroups = [...programGroups].filter(
          oldGroup => oldGroup.id !== groupId
        )
        setProgramGroups(newProgramGroups)
      }
    })
  }


  useEffect(() => {
    getGroups().then(allGroups => allGroups && setProgramGroups(allGroups))
  }, [])

  return (
    <GroupsContext.Provider
      value={{
        programGroups,
        createProgramGroup,
        deleteProgramGroup
      }}
    >
      {children}
    </GroupsContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useProgramGroups(): IGroupsContext {
  const context = useContext(GroupsContext)
  if (!context)
    throw new Error('useProgramGroups must be used within a GroupsProvider')
  const {
    programGroups,
    createProgramGroup,
    deleteProgramGroup,
  } = context
  return {
    programGroups,
    createProgramGroup,
    deleteProgramGroup,
  }
}
