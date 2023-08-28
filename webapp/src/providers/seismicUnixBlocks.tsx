import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'
import { DragDropContext, Droppable, Draggable, DropResult, ResponderProvided } from 'react-beautiful-dnd'


type seismicUnixBlocksType =
  Array<{
    id: string,
    name: string
  }>
type setseismicUnixBlocksType = Dispatch<SetStateAction<seismicUnixBlocksType>>

interface ISeismicUnixBlocksProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISeismicUnixBlocksContext {
  seimicUnixBlocks: seismicUnixBlocksType,
  updateSeimicUnixBlocks: setseismicUnixBlocksType,
  emptyListItems: seismicUnixBlocksType,
  setEmptyListItems: setseismicUnixBlocksType
}

const SeismicUnixBlocksContext = createContext<ISeismicUnixBlocksContext>({
  seimicUnixBlocks: [],
  updateSeimicUnixBlocks: () => undefined,
  emptyListItems: [],
  setEmptyListItems: () => undefined,
})

export default function SeismicUnixBlocksProvider({ children }: ISeismicUnixBlocksProviderProps) {
  const seismicUnixCommand = [
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

    const items = seimicUnixBlocks;
    const [draggedItem] = items.splice(result.source.index, 1);

    if (result.destination.droppableId === 'emptyDroppable') {
      setEmptyListItems(prevItems => [...prevItems, draggedItem]);
    } else {
      items.splice(result.destination.index, 0, draggedItem);
      updateSeimicUnixBlocks(items);
    }
  }

  return (
    <SeismicUnixBlocksContext.Provider
      value={{
        seimicUnixBlocks,
        updateSeimicUnixBlocks,
        emptyListItems,
        setEmptyListItems
      }}
    >
      <DragDropContext onDragEnd={handleOnDragEnd}>
        {children}
      </DragDropContext>
    </SeismicUnixBlocksContext.Provider>
  )
}