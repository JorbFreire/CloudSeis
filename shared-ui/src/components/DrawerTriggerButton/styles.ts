import styled from 'styled-components'
import Button from '@mui/material/Button'

type positionValueType = `${number}px` | "0"

export interface IFloatButtonProps {
  $top?: positionValueType
  $bottom?: positionValueType
  $left?: positionValueType
  $right?: positionValueType
}


export const CustomButton = styled(Button) <IFloatButtonProps>`
  && {
    position: absolute;
    z-index: 10;
    border-radius: 16px;
  }

  ${({ $top }) => $top && `top: ${$top};`}
  ${({ $bottom }) => $bottom && `bottom: ${$bottom};`}
  ${({ $left }) => $left && `left: ${$left};`}
  ${({ $right }) => $right && `right: ${$right};`}
`
