import IconButton from "@mui/material/IconButton";
import DriveFileRenameOutlineRoundedIcon from '@mui/icons-material/DriveFileRenameOutlineRounded';

import DeleteButton from "../DeleteButton";
import { Container, ActionsBox } from "./styles"

interface ILabelContentProps {
  labelText: string
  onRemove(): void
  onUpdate?(): void
}

export default function TreeItemLabelWithActions({
  labelText,
  onRemove,
  onUpdate
}: ILabelContentProps) {
  return (
    <Container>
      {labelText}

      <ActionsBox>
        {onUpdate && (
          <IconButton
            sx={{ zIndex: 1000 }}
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              if (onUpdate)
                onUpdate()
            }}
          >
            <DriveFileRenameOutlineRoundedIcon
              color="primary"
              fontSize="small"
            />
          </IconButton>
        )}

        <DeleteButton
          size="small"
          onRemove={onRemove}
        />
      </ActionsBox>
    </Container>
  )
}
