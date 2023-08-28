import { Droppable, Draggable } from 'react-beautiful-dnd'
import { useSeismicUnixBlocks } from 'providers/seismicUnixBlocks';

interface IWorkflowAreaProps {
  index: number
}

export default function WorkflowArea({ index }: IWorkflowAreaProps) {
  const { seimicUnixBlocks, emptyListItems } = useSeismicUnixBlocks()

  return (
    <div style={{ display: 'flex', margin: '10px', padding: '10px', backgroundColor: 'grey' }}>
      <h3>Variables</h3>
      <Droppable key={index} droppableId={`Variables${index}`}>
        {(provided) => (
          <ul className="variables" {...provided.droppableProps} ref={provided.innerRef}>
            {seimicUnixBlocks.map(({ id, name }, seimicUnixBlocksIndex) => (
              <div style={{ border: '1px solid black', margin: '10px', padding: '10px', backgroundColor: 'white' }}>
                <Draggable key={id} draggableId={`Variable${seimicUnixBlocksIndex}-${id}`} index={seimicUnixBlocksIndex}>
                  {(provided) => (
                    <li ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                      <p>
                        {name}
                      </p>
                    </li>
                  )}
                </Draggable>
              </div>
            ))}
            {provided.placeholder}
          </ul>
        )}
      </Droppable>

      <div style={{ display: 'flex', margin: '10px', padding: '10px', backgroundColor: 'grey' }}></div>
      <h3>SuBlocks</h3>
      <Droppable droppableId="emptyDroppable">
        {(provided) => (
          <ul className="empty-droppable" {...provided.droppableProps} ref={provided.innerRef}>
            {emptyListItems.map((item, index) => (
              <div
                key={`empty-item-${index}`}
                style={{
                  border: '1px solid black',
                  margin: '10px',
                  padding: '10px',
                  backgroundColor: 'lightblue'
                }}
              >
                <p>{item.name}</p>
              </div>
            ))}
            {provided.placeholder}
          </ul>
        )}
      </Droppable>

    </div>
  )
}