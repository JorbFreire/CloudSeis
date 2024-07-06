import { useState } from 'react'
import type { SyntheticEvent } from 'react'


import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import { useLinesStore } from 'store/linesStore';
import { useSelectedWorkflows } from 'providers/SelectedWorkflowsProvider'
import LineChildrenFolder from './LineChildrenFolder'

import { Container } from "./styles"

export default function ProjectTab() {
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId
  } = useSelectedWorkflows()

  const lines = useLinesStore((state) => state.lines)

  const [expanded, setExpanded] = useState<string[]>([]);
  const [selected, setSelected] = useState<string>("");

  const handleToggle = (_: SyntheticEvent, nodeId: string[]) => {
    setExpanded(nodeId);
  };

  const handleSelect = (_: SyntheticEvent, nodeId: string) => {
    const isWorkflow = nodeId.startsWith("workflow")
    const isDataset = nodeId.startsWith("dataset")
    if (!(isWorkflow || isDataset))
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
    ) >= 0

    setSelected(nodeId);
    setSingleSelectedWorkflowId(Number(id))

    if (isAlredySelected)
      return

    setSelectedWorkflows((oldState) => [
      ...oldState,
      {
        id: Number(id),
        name: name,
      }
    ])
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
        {lines.map((line,) => (
          <TreeItem key={line.id} nodeId={`line-${line.id}`} label={line.name}>
            <LineChildrenFolder
              lineId={line.id}
              entityType='workflow'
              data={line.workflows}
            />

            <LineChildrenFolder
              lineId={line.id}
              entityType='dataset'
              data={line.workflows}
            />
          </TreeItem>
        ))}
      </TreeView>
    </Container>
  )
}
