import styled, { css } from 'styled-components'

import TableContainer from '@mui/material/TableContainer'
import TableCell from '@mui/material/TableCell'
import IconButton from '@mui/material/IconButton'

interface ICustomTableCellProps {
  $isShort?: boolean
  $hasDivider?: boolean
}

export const CloseButton = styled(IconButton)`
  position: absolute !important;
  z-index: 10;
  top: -6px;
  left: 16px;
`

export const CustomTableContainer = styled(TableContainer)`
  &.MuiTableContainer-root {
    height: 240px;
  }
`

export const CustomTableCell = styled(TableCell) <ICustomTableCellProps>`
  && {
    ${({ $isShort }) => $isShort && css`width: 120px;`}
    ${({ $isShort }) => !$isShort && css`min-width: 256px;`}
    ${({ variant }) => variant == 'head' && css`
      font-size: 16px;
      text-transform: uppercase;
      text-align: center;
    `}
    ${({ theme, $hasDivider }) => $hasDivider && css`
      border-left: 1px solid ${theme.palette.divider};
    `}
  }
`

export const IconCellContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`
