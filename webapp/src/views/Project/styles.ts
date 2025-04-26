import styled from 'styled-components'
import LoadingButton from '@mui/lab/LoadingButton';

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

export const CommandActionButtonStyled = styled(LoadingButton)`
  display: flex;
  width: fit-content;
  align-self: center;
`
