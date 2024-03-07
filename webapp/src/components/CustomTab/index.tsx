import Tooltip from '@mui/material/Tooltip';
import { Container } from './styles'

export default function CustomTab({
  value,
  label,
  $color,
  $orientation
}: ICustomTabProps) {
  return (
    <Tooltip title={label} key={value}>
      <Container
        value={value}
        label={label}
        $color={$color}
        $orientation={$orientation}
      />
    </Tooltip>

  )
}