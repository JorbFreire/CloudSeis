import { useSortable } from '@dnd-kit/sortable';
import Tooltip from '@mui/material/Tooltip';
import { CSS } from '@dnd-kit/utilities';

import { Container } from './styles'

// todo: turn into generic and make two tab components
export default function CustomTab({
  value,
  label,
  $color = "primary",
  $orientation = "horizontal",
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
    <Tooltip title={label} >
      <Container
        value={value}
        label={label}
        $color={$color}
        $orientation={$orientation}

        ref={setNodeRef}
        style={style}
        {...attributes}
        {...listeners}
      />
    </Tooltip>
  )
}
