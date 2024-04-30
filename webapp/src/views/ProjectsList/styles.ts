import styled from 'styled-components'

import TableCell from '@mui/material/TableCell';

export const Container = styled.div`
  width: 100vw;
  height: 100vh;
  overflow: auto;
`

export const CustomHeadCell = styled(TableCell)`
  &.MuiTableCell-root {
    background-color: #355F55;
    color: #ffffff;
    font-weight: 700;
    font-size: 18px;
    letter-spacing: 2px;
  }
`
