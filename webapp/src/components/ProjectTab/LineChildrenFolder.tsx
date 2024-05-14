import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';

import { useLines } from 'providers/LinesProvider'

interface ILineChildrenFolderProps {
  lineId: number
  entityType: "workflow" | "dataset"
  data: Array<IResumedWorkflow>
}

export default function LineChildrenFolder({
  lineId,
  entityType,
  data,
}: ILineChildrenFolderProps) {
  const { pushNewWorkflowToLine } = useLines()

  const generateNextWorkflowName = () => {
    return (
      "New workflow (" +
      (data[data.length - 1].id + 1) +
      ")"
    )
  }

  return (
    <TreeItem
      nodeId={`${entityType}-from-line-${lineId}`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={workflow.id}
          nodeId={`${entityType}-${workflow.id}-${workflow.name}`}
          label={workflow.name}
        />
      ))}
      {entityType == "workflow" && (
        <Button
          onClick={() => pushNewWorkflowToLine(
            lineId,
            generateNextWorkflowName()
          )}
        >
          New Workflow
        </Button>
      )}
    </TreeItem>
  )
}
