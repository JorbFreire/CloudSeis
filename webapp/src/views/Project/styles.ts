import styled from 'styled-components'

import Button from '@mui/material/Button';
import Fab from '@mui/material/Fab';

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
  width: calc(100% - (256px));
`

export const FloatButton = styled(Fab) <IFloatButtonProps>`
  position: absolute !important;
  z-index: 10;

  ${({ $top }) => $top && `top: ${$top};`}
  ${({ $bottom }) => $bottom && `bottom: ${$bottom};`}
  ${({ $left }) => $left && `left: ${$left};`}
  ${({ $right }) => $right && `right: ${$right};`}
`

export const Text = styled.text`
  color: white;
  padding: 8px 8px;
`

export const RunButton = styled(Button)`
  position: absolute !important;
  z-index: 10;
  bottom: 20px;
  left: 20px;

  width: 100px;
  height: 40px;
`
