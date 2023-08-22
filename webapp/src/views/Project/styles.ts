import styled from 'styled-components'

export const Container = styled.div`
  background-color: #4F4F4F;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 105%;
  height: 100vh;
  gap: 8px;
`

export const VariableContainer = styled.div`
  background-color: #808080;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; 
  align-items: left;
  position: fixed;
  top: 0;
  right: 0; 
  width: 25%;
  height: 35vh;
  gap: 8px;
  z-index: 10;
`

export const Button = styled.button`
  background-color: #C0C0C0;
  color: #000;
  width: fit-content;
  padding: 8px 16px;
  margin-top: 8px;
  margin-bottom: 8px;
`

export const Text = styled.text`
  color: white;
  padding: 8px 8px;
`

const StyledColumns = styled.div`
  display: grid;
  background-color: 1fr 1fr 1fr;
  margin: 10vh auto;
  width: 80%;
  height: 80vh;
  gap: 8px;
`