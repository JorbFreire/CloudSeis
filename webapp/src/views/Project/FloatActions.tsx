import type { Dispatch, SetStateAction } from 'react';

// Fav button icons need futter optimiation and animation
import KeyboardDoubleArrowRightRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowRightRounded';
import KeyboardDoubleArrowLeftRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowLeftRounded';
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';
import KeyboardDoubleArrowUpRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowUpRounded';

import { FloatButton } from './styles'

interface IFloatActions {
  isConsoleOpen: boolean
  setIsConsoleOpen: Dispatch<SetStateAction<boolean>>
  isOptionsDrawerOpen: boolean
  setIsOptionsDrawerOpen: Dispatch<SetStateAction<boolean>>
}

export default function FloatActions({
  isConsoleOpen,
  setIsConsoleOpen,
  isOptionsDrawerOpen,
  setIsOptionsDrawerOpen,
}: IFloatActions) {
  return (
    <>
      <FloatButton
        $top='16px'
        $right={isOptionsDrawerOpen ? "468px" : "16px"}
        onClick={() => setIsOptionsDrawerOpen(!isOptionsDrawerOpen)}
      >
        {isOptionsDrawerOpen ? (
          <KeyboardDoubleArrowRightRoundedIcon />
        ) : (
          <KeyboardDoubleArrowLeftRoundedIcon />
        )}
      </FloatButton>

      <FloatButton
        $bottom={isConsoleOpen ? '60px' : "16px"}
        $left='16px'
        onClick={() => setIsConsoleOpen(!isConsoleOpen)}
      >
        {isConsoleOpen ? (
          <KeyboardDoubleArrowDownRoundedIcon />
        ) : (
          <KeyboardDoubleArrowUpRoundedIcon />
        )}
      </FloatButton>
    </>
  )
}