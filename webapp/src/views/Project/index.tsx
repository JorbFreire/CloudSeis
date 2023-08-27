import { useState, useEffect } from 'react'


import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import Console from '../../components/Console'
import SUFIleInput from '../../components/SUFIleInput'
import { getLinesByProjectID, createNewLine } from '../../services/lineServices'
import { getWorkflowByID, createNewWorkflow } from '../../services/workflowServices'
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

const mockProjectId = "1"

export default function Project({ projectName }: IProjectProps) {
  const [treelines, setTreelines] = useState<Array<ITreeline>>([])
  const [nextId, setNextId] = useState(1)
  const [nextWorkflowId, setNextWorkflowId] = useState(1)
  const [totalWorkflows, setTotalWorkflows] = useState(0)

  const currentTotalWorkflows = totalWorkflows;

  const createLine = async () => {
    const newLine = await createNewLine("1", `Workflow ${nextId}`)
    if (newLine) {
      setTreelines((prevTreelines) => [...prevTreelines, newLine])
      setNextId((prevId) => prevId + 1)
    }
  }

  const createWorkflow = async (lineId: string) => {
    const newWorkflow = await createNewWorkflow(lineId, `Workflow ${nextId}`)

    if (newWorkflow)
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
  }
  
  useEffect(() => {
    (async () => {
      const fetchedLines = await getLinesByProjectID(mockProjectId)
      setTreelines(fetchedLines)
    })()
  }, [])

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
          {Array.from({ length: currentTotalWorkflows }).map((_, index) => (
            <div style={{ display:'flex', margin: '10px', padding: '10px', backgroundColor: 'grey' }}>
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

              <div style={{ display:'flex', margin: '10px', padding: '10px', backgroundColor: 'grey' }}></div>
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
          ))}
      </div>

    </div>
  )
}
