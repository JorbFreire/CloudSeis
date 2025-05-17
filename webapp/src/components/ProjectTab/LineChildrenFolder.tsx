import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';

import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box'

import NoteAddRoundedIcon from '@mui/icons-material/NoteAddRounded';
import DeleteForeverRoundedIcon from '@mui/icons-material/DeleteForeverRounded';

import { defaultWorkflowName } from 'constants/defaults';
import { useLinesStore } from 'store/linesStore';

interface ILineChildrenFolderProps {
  lineId: number
  entityType: "workflow" | "dataset"
  data: Array<IResumedWorkflow>
}

interface ILabelContentProps {
  labelText: string
  onRemove(): void
}

const LabelContent = ({
  labelText,
  onRemove,
}: ILabelContentProps) => (
  <Box
    sx={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }}
  >
    {labelText}
    <IconButton
      sx={{ zIndex: 1000 }}
      size="small"
      onClick={(e) => {
        e.stopPropagation();
        onRemove()
      }}
    >
      <DeleteForeverRoundedIcon
        color="error"
        fontSize="small"
      />
    </IconButton>
  </Box>
)

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
      nodeId={`from-${lineId}-${entityType}`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={`${entityType}-${workflow.id}`}
          nodeId={`${entityType}-${workflow.id}-${workflow.name}`}
          label={
            <LabelContent
              labelText={workflow.name}
              onRemove={() => removeWorkflowFromLine(lineId, workflow.id)}
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
