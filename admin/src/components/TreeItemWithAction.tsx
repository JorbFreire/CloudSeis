import type { ReactNode } from 'react';

import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Box from '@mui/material/Box'
import { IconButton } from '@mui/material';
import DeleteForeverRoundedIcon from '@mui/icons-material/DeleteForeverRounded';

interface ILabelContentProps {
  labelText: string
  deleteAction(): void
}

interface ITreeItemWithActionProps extends ILabelContentProps {
  children: ReactNode
  nodeId: string
}

const LabelContent = ({
  labelText,
  deleteAction
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
      onClick={() => deleteAction()}
    >
      <DeleteForeverRoundedIcon />
    </IconButton>
  </Box>
)

export default function TreeItemWithAction({
  children,
  nodeId,
  labelText,
  deleteAction
}: ITreeItemWithActionProps) {
  return (
    <TreeItem
      nodeId={nodeId}
      label={
        <LabelContent
          labelText={labelText}
          deleteAction={deleteAction}
        />
      }
    >
      {children}
    </TreeItem>
  )
}
