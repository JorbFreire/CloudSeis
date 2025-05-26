import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';
import NoteAddRoundedIcon from '@mui/icons-material/NoteAddRounded';

import { TreeItemLabelWithActions } from 'shared-ui';

import { defaultWorkflowName } from 'constants/defaults';
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
  const {
    pushNewWorkflowToLine,
    removeWorkflowFromLine,
  } = useLinesStore((state) => ({
    pushNewWorkflowToLine: state.pushNewWorkflowToLine,
    removeWorkflowFromLine: state.removeWorkflowFromLine
  }))

  const generateNextWorkflowName = () => {
    if (data.length < 1)
      return defaultWorkflowName

    return (
      `${defaultWorkflowName} (${data.length + 1})`
    )
  }

  return (
    <TreeItem
      itemId={`from-${lineId}-${entityType}`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={`${entityType}-${workflow.id}`}
          itemId={`${entityType}-${workflow.id}-${workflow.name}`}
          label={
            <TreeItemLabelWithActions
              labelText={workflow.name}
              onRemove={() => removeWorkflowFromLine(lineId, workflow.id)}
              onUpdate={(newName) => console.log(newName)}
            />
          }
        />
      ))}
      {entityType == "workflow" && (
        <Button
          onClick={() => pushNewWorkflowToLine(
            lineId,
            generateNextWorkflowName()
          )}
        >
          <NoteAddRoundedIcon />
          New Workflow
        </Button>
      )}
    </TreeItem>
  )
}
