import { createContext, useContext, useState } from 'react'
import type { Dispatch, ReactNode, SetStateAction } from 'react'
import { DragDropContext, DropResult } from 'react-beautiful-dnd'
import { createNewCommand } from 'services/commandServices'


type seismicUnixBlocksType =
  Array<{
    name: string
  }>
interface ISeismicUnixBlocksProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISeismicUnixBlocksContext {
  seimicUnixBlocks: seismicUnixBlocksType,
  commandList: Array<ICommand>,
  setCommandList: Dispatch<SetStateAction<Array<ICommand>>>
}

const SeismicUnixBlocksContext = createContext<ISeismicUnixBlocksContext>({
  seimicUnixBlocks: [],
  commandList: [],
  setCommandList: () => undefined
})

export default function SeismicUnixBlocksProvider({ children }: ISeismicUnixBlocksProviderProps) {
  const seimicUnixBlocks: seismicUnixBlocksType = [
    {
      name: 'suinput'
    },
    {
      name: 'sugain'
    },
    {
      name: 'sufilter'
    },
    {
      name: 'suwind'
    }
  ]

  const [commandList, setCommandList] = useState<Array<ICommand>>([])

  async function handleOnDragEnd(result: DropResult) {
    if (!result.destination) return;

    const items = [...seimicUnixBlocks];
    const [draggedItem] = items.splice(result.source.index, 1);
    console.log("---------- result.source.droppableId ----------")
    console.log(result.source.droppableId)
    const newCommand = await createNewCommand(
      result.source.droppableId,
      draggedItem.name
    )

    if (!newCommand)
      return;
    if (result.destination.droppableId === 'emptyDroppable')
      setCommandList(prevItems => [...prevItems, newCommand]);
  }

  return (
    <SeismicUnixBlocksContext.Provider
      value={{
        seimicUnixBlocks,
        commandList,
        setCommandList
      }}
    >
      <DragDropContext onDragEnd={handleOnDragEnd}>
        {children}
      </DragDropContext>
    </SeismicUnixBlocksContext.Provider>
  )
}

export function useSeismicUnixBlocks(): ISeismicUnixBlocksContext {
  const context = useContext(SeismicUnixBlocksContext)
  if (!context)
    throw new Error('useSeismicUnixBlocks must be used within a SeismicUnixBlocksProvider')
  const { seimicUnixBlocks, commandList, setCommandList } = context
  return { seimicUnixBlocks, commandList, setCommandList }
}
