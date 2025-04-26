import styled from 'styled-components'
import Fab from '@mui/material/Fab'

type positionValueType = `${number}px` | "0"

export interface IFloatButtonProps {
  $top?: positionValueType
  $bottom?: positionValueType
  $left?: positionValueType
  $right?: positionValueType
}


export const CustomFab = styled(Fab) <IFloatButtonProps>`
  && {
    position: absolute;
    z-index: 10;
  }

  ${({ $top }) => $top && `top: ${$top};`}
  ${({ $bottom }) => $bottom && `bottom: ${$bottom};`}
  ${({ $left }) => $left && `left: ${$left};`}
  ${({ $right }) => $right && `right: ${$right};`}
`
