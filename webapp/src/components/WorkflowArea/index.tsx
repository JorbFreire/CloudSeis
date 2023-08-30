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
import { getWorkflowByID } from 'services/workflowServices';

interface IWorkflowAreaProps {
  workflowId: string
  setSelectedWorkFlowsIds: Dispatch<SetStateAction<Array<string>>>
}

export default function WorkflowArea({
  workflowId,
  setSelectedWorkFlowsIds
}: IWorkflowAreaProps) {
  const { seimicUnixBlocks, commandList, setCommandList } = useSeismicUnixBlocks()

  const closeWorkFlow = () => {
    setSelectedWorkFlowsIds((prev) =>
      prev.filter(value => value !== workflowId)
    )
  }

  const loadWorkflow = async () => {
    const workflow = await getWorkflowByID(workflowId)
    if (workflow)
      setCommandList(workflow.commands)
  }

  return (
    <Container>
      <DroppableWrapper>
        <CloseButton onClick={closeWorkFlow}> Fechar </CloseButton>
        <h3>Programas Disponiveis</h3>
        <Droppable key={workflowId} isDropDisabled={true} droppableId={`w${workflowId}`}>
          {(provided) => (
            <ul className="variables" {...provided.droppableProps} ref={provided.innerRef}>
              {seimicUnixBlocks.map(({ name }, seimicUnixBlocksIndex) => (
                <Draggable key={name} draggableId={`unix-blocks-list${seimicUnixBlocksIndex}-${name}`} index={seimicUnixBlocksIndex}>
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
        <Droppable droppableId={`wwww${workflowId}`}>
          {(provided) => (
            <ul className="empty-droppable" {...provided.droppableProps} ref={provided.innerRef}>
              {commandList.map(({ id, name }, seimicUnixBlocksIndex) => (
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
