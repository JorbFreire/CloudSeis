import styled from "styled-components";
import Button from "@mui/material/Button";

export const Container = styled.div`
  position: relative;
  display: flex;
  width: fit-content;
  flex-direction: row;
  margin: 10px;
  gap: 40px;
  background-color: grey;

  & > :not(:first-child) {
    padding: 10px;
    padding-top: 64px;
  }
`

export const ActionsContainer = styled.div`
  position: absolute;
  display: flex;
  justify-content: space-between;
  width: 100%;
`

export const CloseButton = styled(Button)`
  background-color: #AA4344 !important;
  color: #fff !important;
`

export const ExecuteButton = styled(Button)`
  background-color: #3065AC !important;
  color: #fff !important;
`

export const DroppableWrapper = styled.div``

export const UnixBlockItem = styled.div`
  display: flex;
  gap: 12px;
  border: 1px solid black;
  margin: 10px;
  padding: 10px;
  background-color: white;
`

export const EditUnixParamsButton = styled.button`
  padding: 4px;
`
