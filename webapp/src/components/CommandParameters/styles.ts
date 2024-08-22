import styled from "styled-components"
import TextField from "@mui/material/TextField"
import Button from "@mui/material/Button"
import Tooltip from "@mui/material/Tooltip"

export const Container = styled.form`
  display: flex;
  flex-direction: column;
  max-width: 512px;
`

export const CustomTextField = styled(TextField)`
  :not(:last-of-type) {
    margin-bottom: 32px !important;
  }
  input {
    color: #fff;
  }
  label {
    font-size: 22px;
    transform: translate(14px, -16px) scale(100%);
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
