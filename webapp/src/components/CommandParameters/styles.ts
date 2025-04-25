import styled from "styled-components"
import TextField from "@mui/material/TextField"
import Button from "@mui/material/Button"
import Tooltip from "@mui/material/Tooltip"

export const Container = styled.form`
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;

  height: 100%;
  width: 100%;
  padding-top: 8px;
  gap: 16px;
`

export const CustomTextField = styled(TextField)`
  label {
    font-size: 20px;
    transform: translate(14px, -16px) scale(100%);
  }
  input {
    padding-top: 8px;
    padding-bottom: 4px;
  }
  legend {
    font-size: 22px;
  }
`

export const CustomButton = styled(Button)`
  :not(:only-child) {
    margin-top: 16px;
  }
`

export const CustomTooltip = styled(Tooltip)``
