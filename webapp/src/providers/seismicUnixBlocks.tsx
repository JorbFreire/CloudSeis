import { createContext, useContext, useState } from 'react'
import type { ReactNode } from 'react'
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
  emptyListItems: Array<ICommand>,
}

const SeismicUnixBlocksContext = createContext<ISeismicUnixBlocksContext>({
  seimicUnixBlocks: [],
  emptyListItems: [],
})

export default function SeismicUnixBlocksProvider({ children }: ISeismicUnixBlocksProviderProps) {
  const seismicUnixCommand: seismicUnixBlocksType = [
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

  const [seimicUnixBlocks, _] = useState<seismicUnixBlocksType>(seismicUnixCommand)
  const [emptyListItems, setEmptyListItems] = useState<Array<ICommand>>([])

  async function handleOnDragEnd(result: DropResult) {
    if (!result.destination) return;

    const items = [...seimicUnixBlocks];
    const [draggedItem] = items.splice(result.source.index, 1);
    const newCommand = await createNewCommand()

    if (result.destination.droppableId === 'emptyDroppable')
      setEmptyListItems(prevItems => [...prevItems, draggedItem]);
  }

  return (
    <SeismicUnixBlocksContext.Provider
      value={{
        seimicUnixBlocks,
        emptyListItems,
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
  const { seimicUnixBlocks, emptyListItems } = context
  return { seimicUnixBlocks, emptyListItems }
}
