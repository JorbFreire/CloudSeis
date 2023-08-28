import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'
import { DragDropContext, Droppable, Draggable, DropResult, ResponderProvided } from 'react-beautiful-dnd'


type seismicUnixBlocksType =
  Array<{
    id: string,
    name: string
  }>

type readonlySeismicUnixBlocksType =
  Array<{
    readonly id: string,
    readonly name: string
  }>

interface ISeismicUnixBlocksProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISeismicUnixBlocksContext {
  seimicUnixBlocks: seismicUnixBlocksType,
  emptyListItems: seismicUnixBlocksType,
}

const SeismicUnixBlocksContext = createContext<ISeismicUnixBlocksContext>({
  seimicUnixBlocks: [],
  emptyListItems: [],
})

export default function SeismicUnixBlocksProvider({ children }: ISeismicUnixBlocksProviderProps) {
  const seismicUnixCommand: readonlySeismicUnixBlocksType = [
    {
      id: 'suinput',
      name: 'suinput'
    },
    {
      id: 'sugain',
      name: 'sugain'
    },
    {
      id: 'sufilter',
      name: 'sufilter'
    },
    {
      id: 'suwind',
      name: 'suwind'
    }
  ]

  const [seimicUnixBlocks, updateSeimicUnixBlocks] = useState<seismicUnixBlocksType>(seismicUnixCommand)
  const [emptyListItems, setEmptyListItems] = useState<seismicUnixBlocksType>([])

  function handleOnDragEnd(result: DropResult) {
    if (!result.destination) return;

    const items = [...seimicUnixBlocks];
    // this is splice is afecting a point and should only afect a copy
    const [draggedItem] = items.splice(result.source.index, 1);

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
