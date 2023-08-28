import { useState, useEffect } from 'react'

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import Console from '../../components/Console'
import CommandOptionsDrawer from 'components/CommandOptionsDrawer';
import WorkflowArea from 'components/WorkflowArea';
import SUFIleInput from '../../components/SUFIleInput'
import { getLinesByProjectID, createNewLine } from '../../services/lineServices'
import { createNewWorkflow } from '../../services/workflowServices'
import { Container, ProjectMenuBox, Button } from './styles'


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
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [isOptionsDrawerOpen, setIsOptionsDrawerOpen] = useState(true)

  const [treelines, setTreelines] = useState<Array<ITreeline>>([])
  const [selectedWorkFlowsIds, setSelectedWorkFlowsIds] = useState<Array<string>>([])
  const [nextId, setNextId] = useState(1)

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
  }

  useEffect(() => {
    (async () => {
      const fetchedLines = await getLinesByProjectID(mockProjectId)
      setTreelines(fetchedLines)
    })()
  }, [])

  return (
    <>
      <Container>
        <ProjectMenuBox>
          <TreeView
            aria-label="file system navigator"
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ChevronRightIcon />}
            sx={{ height: 240, flexGrow: 1, maxWidth: 400, overflowY: 'auto' }}
          >
            <Button onClick={() => setIsOptionsDrawerOpen(!isOptionsDrawerOpen)}>
              {isOptionsDrawerOpen ? "Fechar " : "Abrir "} Parametros
            </Button>
            <Button onClick={() => setIsConsoleOpen(!isConsoleOpen)}>
              {isConsoleOpen ? "Fechar " : "Abrir "} Console
            </Button>
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
                  <TreeItem
                    onClick={() => setSelectedWorkFlowsIds((prev) => [...prev, workflow.id])}
                    key={`w${workflow.id}`}
                    nodeId={`w${workflow.id}`}
                    label={`Workflow ${workflow.id}`}
                  />
                ))}
              </TreeItem>
            ))}

            <SUFIleInput projectName={projectName || ""} />
          </TreeView>

          <h1>{projectName}</h1>
        </ProjectMenuBox>

        {selectedWorkFlowsIds.map((selectedWorkFlowsId) => (
          <WorkflowArea
            workflowId={selectedWorkFlowsId}
            setSelectedWorkFlowsIds={setSelectedWorkFlowsIds}
          />
        ))}
      </Container>


      <Console isOpen={isConsoleOpen} setIsOpen={setIsConsoleOpen} />
      <CommandOptionsDrawer
        isOpen={isOptionsDrawerOpen}
        setIsOpen={setIsOptionsDrawerOpen}
      />
    </>
  )
}
