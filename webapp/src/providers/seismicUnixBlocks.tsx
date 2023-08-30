import { createContext, useContext, useState } from 'react'
import type { Dispatch, ReactNode, SetStateAction } from 'react'
import { DragDropContext, DropResult } from 'react-beautiful-dnd'
import { createNewCommand, updateCommandsOrder } from 'services/commandServices'


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
    if (!result.destination || result.reason === "CANCEL") return;

    const isCreateCommandTrigger = Boolean(result.draggableId.includes("unix-blocks-list"))
    const isOrderUpdateTrigger = !isCreateCommandTrigger

    const workflowId = result.source.droppableId.replaceAll("w", "")
    const commandIndex = result.source.index

    if (isOrderUpdateTrigger) {
      const newIndex = result.destination.index
      if (newIndex == commandIndex) return;

      const newCommandList = [...commandList]

      const draggedItem = newCommandList.splice(commandIndex, 1)
      newCommandList.splice(newIndex, 0, draggedItem[0])

      const newOrder = newCommandList.map((command) => command.id)
      await updateCommandsOrder(workflowId, newOrder)

      setCommandList(newCommandList)
    }

    if (isCreateCommandTrigger) {
      const items = [...seimicUnixBlocks];
      const [draggedItem] = items.splice(commandIndex, 1);

      const newCommand = await createNewCommand(
        workflowId,
        draggedItem.name
      )

      if (!newCommand)
        return;
      if (result.destination.droppableId.includes("wwww"))
        setCommandList(prevItems => [...prevItems, newCommand]);
    }
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
