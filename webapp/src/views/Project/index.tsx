import { useState } from 'react'

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import Console from '../../components/Console'
import SUFIleInput from '../../components/SUFIleInput'
import { Container, Button, VariableContainer } from './styles'
import { DragDropContext, Droppable, Draggable, DropResult, ResponderProvided } from 'react-beautiful-dnd'

interface IProjectProps {
  projectName?: string
  projectId?: string
}

interface ITreeline {
  id: string
  workflows: Array<IWorkflow>
}

interface IWorkflow {
  id: string
}

const seismicUnixVariables = [
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

export default function Project({ projectName }: IProjectProps) {
  const [treelines, setTreelines] = useState<Array<ITreeline>>([])
  const [nextId, setNextId] = useState(1)
  const [nextWorkflowId, setNextWorkflowId] = useState(1)
  const [totalWorkflows, setTotalWorkflows] = useState(0)
  const [variables, updateVariables] = useState(seismicUnixVariables)

  const currentTotalWorkflows = totalWorkflows;

  const createLine = () => {
    const newLine = {
      id: String(nextId),
      workflows: []
    }

    setTreelines((prevTreelines) => [...prevTreelines, newLine])
    setNextId((prevId) => prevId + 1)
  }

  const createWorkflow = (lineId: string) => {
    const newWorkflow = {
      id: String(nextWorkflowId)
    }

    setTreelines((prevTreelines) =>
      prevTreelines.map((treeline) => {
        if (treeline.id === lineId) {
          return {
            ...treeline,
            workflows: [...treeline.workflows, newWorkflow]
          }
        }
        return treeline
      })
    )

    setNextWorkflowId((prevId) => prevId + 1)
    setTotalWorkflows((prevTotal) => prevTotal + 1)

    console.log("Updated Treelines:", treelines);

    console.log("Total Workflows:", totalWorkflows);
  }

  function handleOnDragEnd(result: DropResult) {
    if (!result.destination) return;

    const items = Array.from(variables)
    const [reoredItems] = items.splice(result.source.index, 1)
    items.splice(result.destination.index, 0, reoredItems)

    updateVariables(items)
  }

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column'}}>
        <Container>
          <TreeView
            aria-label="file system navigator"
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ChevronRightIcon />}
            sx={{ height: 240, flexGrow: 1, maxWidth: 400, overflowY: 'auto' }}
          >
            <Button onClick={createLine}>
              Create Line
            </Button>

            {treelines.map((treeline) => (
              <TreeItem key={treeline.id} nodeId={treeline.id} label={`Line ${treeline.id}`}>
                <Button className='workFlowButton' onClick={() => createWorkflow(treeline.id)}>
                  Create Workflow
                </Button>
                {/* tree item nodeId can never be equal inside the same tree view */}
                {treeline.workflows.map((workflow) => (
                  <TreeItem key={`w${workflow.id}`} nodeId={`w${workflow.id}`} label={`Workflow ${workflow.id}`} />
                ))}
              </TreeItem>
            ))}

            <SUFIleInput projectName={projectName || ""} />
          </TreeView>

          <h1>{projectName}</h1>
        </Container>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column'}}>
        <VariableContainer>
          <h4>
            BotoView
          </h4>
        </VariableContainer>
      </div>

      <div style={{ display: 'flex', flexDirection: 'row'}}>
        <Console messages={[]} />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
        <DragDropContext onDragEnd={handleOnDragEnd}>
          {Array.from({ length: currentTotalWorkflows }).map((_, index) => (
            <Droppable key={index} droppableId={`Variables${index}`}>
              {(provided) => (
                <ul className="variables" {...provided.droppableProps} ref={provided.innerRef}>
                  {variables.map(({ id, name }, variableIndex) => (
                    <Draggable key={id} draggableId={`Variable${variableIndex}-${id}`} index={variableIndex}>
                      {(provided) => (
                        <li ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                          <p>
                            {name}
                          </p>
                        </li>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </ul>
              )}
            </Droppable>
          ))}
        </DragDropContext>
      </div>
    </div>
  )
}
