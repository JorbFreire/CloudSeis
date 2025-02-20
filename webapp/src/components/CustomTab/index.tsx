import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import Tooltip from '@mui/material/Tooltip';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import CommentsDisabledRoundedIcon from '@mui/icons-material/CommentsDisabledRounded';

import { updateCommandIsActive } from 'services/commandServices';

import {
  Container,
  TabBody,
  ActionButtonsContainer,
  ActionButton
} from './styles'

// use is_active to turn down opacity
// todo: turn into generic and make two tab components
export default function CustomTab({
  // *** value is usually the related item ID
  value,
  label,
  onRemove,
  $color = "primary",
  $orientation = "horizontal",
  $isActive = true,
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

  const handleUpdateCommandIsActive = () => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    updateCommandIsActive(token, value)
  }

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
            $isActive={$isActive}

            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
          />
          {$orientation == "vertical" && Number.isInteger(value) && (
            <ActionButtonsContainer>
              <ActionButton onClick={handleUpdateCommandIsActive}>
                <CommentsDisabledRoundedIcon />
              </ActionButton>
              <ActionButton onClick={onRemove}>
                <CloseRoundedIcon />
              </ActionButton>
            </ActionButtonsContainer>
          )}
          {/*  */}
        </Container>
      </Tooltip>
    </>
  )
}
