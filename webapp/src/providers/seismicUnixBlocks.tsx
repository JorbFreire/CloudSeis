import { createContext, useContext, useState  } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'
import { DragDropContext, Droppable, Draggable, DropResult, ResponderProvided } from 'react-beautiful-dnd'

type seismicUnixBlocksType =
  Array<{
    id: string,
    name: string
  }> | undefined
type setseismicUnixBlocksType = Dispatch<SetStateAction<seismicUnixBlocksType>>

interface ISeismicUnixBlocksProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ISeismicUnixBlocksContext {
  seimicUnixBlocks: seismicUnixBlocksType,
  updateSeimicUnixBlocks: seismicUnixBlocksType,
  emptyListItems: seismicUnixBlocksType,
  setEmptyListItems: seismicUnixBlocksType
}

const SeismicUnixBlocksContext = createContext<ISeismicUnixBlocksContext>({})

export default function SeismicUnixBlocksProvider({ children }) {

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

  const [seimicUnixBlocks, updateSeimicUnixBlocks] = useState(seismicUnixCommand)
  const [emptyListItems, setEmptyListItems] = useState<Array<{ id: string; name: string }>>([])

  function handleOnDragEnd(result: DropResult) {
    if (!result.destination) return;

    const items = Array.from(seimicUnixBlocks);
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