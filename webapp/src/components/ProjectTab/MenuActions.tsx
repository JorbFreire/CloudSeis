import Button from '@mui/material/Button';
import { useLocation, useNavigate } from '@tanstack/react-location';

import { defaultLineName } from 'constants/defaults';
import { useLinesStore } from 'store/linesStore';

import { CustomButtonGroup } from './styles'

export default function MenuActions() {
  const location = useLocation()
  const navigate = useNavigate()

  const projectId = Number(location.current.pathname.split('/')[2])

  const {
    lines,
    saveNewLine
  } = useLinesStore((state) => ({
    lines: state.lines,
    saveNewLine: state.saveNewLine
  }))

  const generateNextLineName = () => {
    if (lines.length < 1)
      return defaultLineName

    return (
      `${defaultLineName} (${lines.length + 1})`
    )
  }


  return (
    <CustomButtonGroup
      fullWidth
      variant='contained'
    >
      <Button
        onClick={() => saveNewLine(
          projectId,
          generateNextLineName()
        )}
      >
        New Line
      </Button>
      <Button onClick={() => navigate({ to: "/projects" })}>
        Projects
      </Button>
      <Button onClick={() => navigate({ to: "/login" })}>
        Logout
      </Button>
    </CustomButtonGroup >
  )
}