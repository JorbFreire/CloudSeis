import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';

import { useLinesStore } from 'store/linesStore';

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
  const pushNewWorkflowToLine = useLinesStore((state) => state.pushNewWorkflowToLine)

  const generateNextWorkflowName = () => {
    if (data.length < 1)
      return "New workflow"

    return (
      `New workflow (${data.length + 1})`
    )
  }

  return (
    <TreeItem
      nodeId={`from-${lineId}-${entityType}`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={`${entityType}-${workflow.id}`}
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
