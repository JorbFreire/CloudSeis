import type { ReactNode } from 'react';

import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Box from '@mui/material/Box'
import DeleteButton from '../components/DeleteButton';
import Button from '@mui/material/Button';

import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

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


    <DeleteButton onClick={deleteAction} size='small' />
  </Box>
)

export default function TreeItemWithAction({
  children,
  nodeId,
  labelText,
  deleteAction
}: ITreeItemWithActionProps) {
  const { setSelectedProgram } = useSelectedProgramCommand()
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
      <Button variant="contained" onClick={() => setSelectedProgram(null)}>
        Novo programa
      </Button>
      {children}
    </TreeItem>
  )
}
