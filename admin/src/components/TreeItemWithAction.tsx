import type { ReactNode } from 'react';

import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';

import { TreeItemLabelWithActions } from 'shared-ui';

import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

interface ILabelContentProps {
  labelText: string
  deleteAction(): void
}

interface ITreeItemWithActionProps extends ILabelContentProps {
  children: ReactNode
  nodeId: string
}

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
        <TreeItemLabelWithActions
          labelText={labelText}
          onRemove={deleteAction}
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
