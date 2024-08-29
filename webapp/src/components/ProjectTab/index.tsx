import { useState } from 'react'
import type { SyntheticEvent } from 'react'
import { useTimeout } from 'react-use';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import { useLinesStore } from 'store/linesStore';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import LineChildrenFolder from './LineChildrenFolder'
import DataSetsFolder from './DataSetsFolder'

import { Container } from "./styles"

export default function ProjectTab() {
  const lines = useLinesStore((state) => state.lines)
  const {
    selectWorkflow,
  } = useSelectedWorkflowsStore((state) => ({
    selectWorkflow: state.selectWorkflow,
  }))

  const [expanded, setExpanded] = useState<string[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [isAllowToSelect, _, resetAllowToSelectTimer] = useTimeout(1000);

  const handleToggle = (_: SyntheticEvent, nodeId: string[]) => {
    setExpanded(nodeId);
  };

  const handleSelect = (_: SyntheticEvent, nodeId: string) => {
    if (!isAllowToSelect())
      return
    resetAllowToSelectTimer()

    const isWorkflow = nodeId.startsWith("workflow")
    const isDataset = nodeId.startsWith("dataset")


    if (!(isWorkflow || isDataset))
      return
    const [key, id, name] = nodeId.split("-")

    if (key !== "workflow" || !id || !name)
      return

    selectWorkflow(Number(id), () => setSelected(nodeId))
  }

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


            <DataSetsFolder line={line} />
          </TreeItem>
        ))}
      </TreeView>
    </Container>
  )
}
