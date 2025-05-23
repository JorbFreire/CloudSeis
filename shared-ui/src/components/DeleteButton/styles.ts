import styled from 'styled-components'

import IconButton from '@mui/material/IconButton'
import Button from '@mui/material/Button'

interface ICustomButtonProps {
  $isHidden: boolean
}

interface ICustomIconButtonProps {
  $isHoverDisable: boolean
}

export const CustomIconButton = styled(IconButton) <ICustomIconButtonProps>`
  && {
    z-index: 1000;
    cursor: ${({ $isHoverDisable }) => $isHoverDisable ? "inherit" : "pointer"};
  }
`

export const CustomButton = styled(Button) <ICustomButtonProps>`
  && {
    position: absolute;
    right: 0;
    display: ${({ $isHidden }) => !$isHidden ? "flex" : "none"};
  }
`
