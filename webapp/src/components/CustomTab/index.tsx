import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import Tooltip from '@mui/material/Tooltip';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded'

import {
  Container,
  TabBody,
  ActionButton
} from './styles'

// todo: turn into generic and make two tab components
export default function CustomTab({
  value,
  label,
  onRemove,
  $color = "primary",
  $orientation = "horizontal",
  // *** for some reason, "...props" is necessery for tabs component ***
  ...props
}: ICustomTabProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: value });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <>
      <Tooltip title={label} >
        <Container>
          <TabBody
            {...props}
            value={value}
            label={label}
            $color={$color}
            $orientation={$orientation}

            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
          />
          {$orientation == "vertical" && (
            <ActionButton onClick={onRemove}>
              <CloseRoundedIcon />
            </ActionButton>
          )}
        </Container>
      </Tooltip>
    </>
  )
}
