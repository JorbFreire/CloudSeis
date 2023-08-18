import { useState } from 'react'

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import Console from '../../components/Console'
import SUFIleInput from '../../components/SUFIleInput'
import { createNewLine } from '../../services/lineServices'
import { createNewWorkflow } from '../../services/workflowServices'
import { Container, Button, VariableContainer } from './styles'
interface IProjectProps {
  projectName?: string
  projectId?: string
}

export default function Project({ projectName }: IProjectProps) {
  const [treelines, setTreelines] = useState<Array<ILine>>([])
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

  const createWorkflow = (lineId: string) => {
    const newWorkflow = {
      id: String(nextWorkflowId),
      name: "name"
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

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column', height: '80vh' }}>
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
                {treeline.workflows.map((workflow) => (
                  <TreeItem key={workflow.id} nodeId={workflow.id} label={`Workflow ${workflow.id}`} />
                ))}
              </TreeItem>
            ))}

            <SUFIleInput projectName={projectName || ""} />
          </TreeView>

          <h1>{projectName}</h1>
        </Container>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <VariableContainer>
          <h4>
            BotoView
          </h4>
        </VariableContainer>
      </div>

      <div style={{ display: 'flex', flexDirection: 'row', height: '100vh' }}>
        <Console messages={[]} />
      </div>

      {Array.from({ length: currentTotalWorkflows }).map((_, index) => (
        <div
          key={index}
          style={{ border: '1px solid black', margin: '10px', padding: '10px', backgroundColor: 'blue' }}
        >
          <h1>Workflow</h1>
          Workflow {index + 1} Content
        </div>
      ))}

    </div>
  )
}
