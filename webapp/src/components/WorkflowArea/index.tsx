import type { Dispatch, SetStateAction } from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd'
import { useSeismicUnixBlocks } from 'providers/seismicUnixBlocks';

import {
  Container,
  CloseButton,
  DroppableWrapper,
  UnixBlockItem,
  EditUnixParamsButton
} from './styles';

interface IWorkflowAreaProps {
  workflowId: string
  setSelectedWorkFlowsIds: Dispatch<SetStateAction<Array<string>>>
}

export default function WorkflowArea({
  workflowId,
  setSelectedWorkFlowsIds
}: IWorkflowAreaProps) {
  const { seimicUnixBlocks, emptyListItems } = useSeismicUnixBlocks()
  const closeWorkFlow = () => {
    setSelectedWorkFlowsIds((prev) =>
      prev.filter(value => value !== workflowId)
    )
  }
  return (
    <Container>
      <DroppableWrapper>
        <CloseButton onClick={closeWorkFlow}> Fechar </CloseButton>
        <h3>Programas Disponiveis</h3>
        <Droppable key={workflowId} isDropDisabled={true} droppableId={`Variables${workflowId}`}>
          {(provided) => (
            <ul className="variables" {...provided.droppableProps} ref={provided.innerRef}>
              {seimicUnixBlocks.map(({ name }, seimicUnixBlocksIndex) => (
                <Draggable key={name} draggableId={`Variable${seimicUnixBlocksIndex}-${name}`} index={seimicUnixBlocksIndex}>
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

      <DroppableWrapper>
        <h3>Workflow</h3>
        <Droppable droppableId="emptyDroppable">
          {(provided) => (
            <ul className="empty-droppable" {...provided.droppableProps} ref={provided.innerRef}>
              {emptyListItems.map(({ id, name }, seimicUnixBlocksIndex) => (
                <Draggable key={id} draggableId={`Workflow${seimicUnixBlocksIndex}-${id}`} index={seimicUnixBlocksIndex}>
                  {(provided) => (
                    <UnixBlockItem
                      key={`empty-item-${workflowId}`}
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
