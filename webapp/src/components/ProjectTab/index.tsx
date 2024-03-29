import { useState } from 'react'
import type { SyntheticEvent } from 'react'

import { useSelectedWorkflows } from 'providers/SelectedWorkflowsProvider'

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import { Container } from "./styles"

const mockLinesList: Array<ILine> = Array(10).fill({}).map((_, index) => (
  {
    id: index,
    projectId: 1,
    name: `line => ${index}`,
    // todo: missing datasets here
    workflows: Array(10).fill({}).map((_, index) => (
      {
        id: index,
        name: `workflow => ${index}`,
      }
    )),
  }
))

export default function ProjectTab() {
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId
  } = useSelectedWorkflows()

  const [expanded, setExpanded] = useState<string[]>([]);
  const [selected, setSelected] = useState<string>("");

  const handleToggle = (_: SyntheticEvent, nodeId: string[]) => {
    setExpanded(nodeId);
  };

  const handleSelect = (_: SyntheticEvent, nodeId: string) => {
    if (!nodeId.includes("workflow"))
      return
    const [key, id, name] = nodeId.split("-")

    if (singleSelectedWorkflowId != undefined) {
      const isAlredySingleSelected = id == singleSelectedWorkflowId.toString();
      if (isAlredySingleSelected)
        return
    }

    if (key !== "workflow" || !id || !name)
      return

    const isAlredySelected = selectedWorkflows.findIndex(
      (element) => element.id == Number(id)
    ) > 0
    if (isAlredySelected)
      return

    setSelectedWorkflows((oldState) => [
      ...oldState,
      {
        id: Number(id),
        name: name,
      }
    ])
    setSelected(nodeId);
    setSingleSelectedWorkflowId(Number(id))
  };


  return (
    <Container>
      <TreeView
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        expanded={expanded}
        selected={selected}
        onNodeToggle={handleToggle}
        onNodeSelect={handleSelect}
      >
        {mockLinesList.map((line,) => (
          <TreeItem key={line.id} nodeId={`line-${line.id}`} label={line.name}>
            <TreeItem
              nodeId={`ws_from-line-${line.id}`}
              label="workflows"
            >
              {line.workflows.map((workflow) => (
                <TreeItem
                  key={workflow.id}
                  nodeId={`workflow-${workflow.id}-${workflow.name}`}
                  label={workflow.name}
                />
              ))}
            </TreeItem>

            <TreeItem
              nodeId={`ds_from-line-${line.id}`}
              label="datasets"
            >
              {line.workflows.map((workflow) => (
                <TreeItem
                  key={workflow.id}
                  nodeId={`dataset-${workflow.id}-${workflow.name}`}
                  label={workflow.name}
                />
              ))}
            </TreeItem>
          </TreeItem>
        ))}
      </TreeView>
    </Container>
  )
}
