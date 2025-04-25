import styled from 'styled-components'
import Fab from '@mui/material/Fab';
import LoadingButton from '@mui/lab/LoadingButton';

type positionValueType = `${number}px` | "0"

interface IFloatButtonProps {
  $top?: positionValueType
  $bottom?: positionValueType
  $left?: positionValueType
  $right?: positionValueType
}

export const Container = styled.div`
  position: relative;
  display: flex;
  width: 100vw;
  height: 100vh;
`

export const SelectedWorkflowsContainer = styled.div`
  position: relative;
  display: flex;
  width: calc(100% - (320px));
`

export const FloatButton = styled(Fab) <IFloatButtonProps>`
  position: absolute !important;
  z-index: 10;

  ${({ $top }) => $top && `top: ${$top};`}
  ${({ $bottom }) => $bottom && `bottom: ${$bottom};`}
  ${({ $left }) => $left && `left: ${$left};`}
  ${({ $right }) => $right && `right: ${$right};`}
`

export const CommandActionButtonStyled = styled(LoadingButton)`
  display: flex;
  width: fit-content;
  align-self: center;
`
