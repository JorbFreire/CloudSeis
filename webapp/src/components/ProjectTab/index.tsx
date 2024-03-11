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
    setSelectedWorkflows,
    setSingleSelectedWorkflowId
  } = useSelectedWorkflows()

  const [expanded, setExpanded] = useState<string[]>([]);
  const [selected, setSelected] = useState<string>("");

  const handleToggle = (event: SyntheticEvent, nodeIds: string[]) => {
    setExpanded(nodeIds);
  };

  const handleSelect = (event: SyntheticEvent, nodeIds: string) => {
    if (nodeIds.includes("workflow")) {
      const [_, id] = nodeIds.split("-")
      setSelectedWorkflows((oldState) => [
        ...oldState,
        {
          id: Number(id),
          name: "a",
        }
      ])
      setSingleSelectedWorkflowId(Number(id))
      setSelected(nodeIds);
    }
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
                  nodeId={`workflow-${workflow.id}`}
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
                  nodeId={`dataset-${workflow.id}`}
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
