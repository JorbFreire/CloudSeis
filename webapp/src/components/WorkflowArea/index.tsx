import { Droppable, Draggable } from 'react-beautiful-dnd'
import { useSeismicUnixBlocks } from 'providers/seismicUnixBlocks';

import {
  Container,
  DroppableWrapper,
  UnixBlockItem,
  EditUnixParamsButton
} from './styles';

interface IWorkflowAreaProps {
  index: number
}

export default function WorkflowArea({ index }: IWorkflowAreaProps) {
  const { seimicUnixBlocks, emptyListItems } = useSeismicUnixBlocks()

  return (
    <Container>
      <DroppableWrapper>
        <h3>Programas Disponiveis</h3>
        <Droppable key={index} isDropDisabled={true} droppableId={`Variables${index}`}>
          {(provided) => (
            <ul className="variables" {...provided.droppableProps} ref={provided.innerRef}>
              {seimicUnixBlocks.map(({ id, name }, seimicUnixBlocksIndex) => (
                <Draggable key={id} draggableId={`Variable${seimicUnixBlocksIndex}-${id}`} index={seimicUnixBlocksIndex}>
                  {(provided) => (
                    <UnixBlockItem ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} >
                      {name}
                    </UnixBlockItem>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ul>
          )}
        </Droppable>
      </DroppableWrapper>

      <button onClick={() => console.log(seimicUnixBlocks)}>
        log
      </button>

      <DroppableWrapper>
        <h3>Workflow</h3>
        <Droppable droppableId="emptyDroppable">
          {(provided) => (
            <ul className="empty-droppable" {...provided.droppableProps} ref={provided.innerRef}>
              {emptyListItems.map(({ id, name }, seimicUnixBlocksIndex) => (
                <Draggable key={id} draggableId={`Workflow${seimicUnixBlocksIndex}-${id}`} index={seimicUnixBlocksIndex}>
                  {(provided) => (
                    <UnixBlockItem
                      key={`empty-item-${index}`}
                      style={{
                        backgroundColor: 'lightblue'
                      }}
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    >
                      {name}
                      <EditUnixParamsButton>
                        Editar Parametros
                      </EditUnixParamsButton>
                    </UnixBlockItem>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ul>
          )}
        </Droppable>
      </DroppableWrapper>
    </Container>
  )
}
