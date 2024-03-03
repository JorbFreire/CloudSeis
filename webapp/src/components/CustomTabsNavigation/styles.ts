import styled from "styled-components";

import Tab from '@mui/material/Tab';

export type orientationType = 'horizontal' | 'vertical'
interface IContainerProps {
  orientation: orientationType
}

function getContainerDirection(orientation: orientationType) {
  if (orientation == "horizontal")
    return "column"
  if (orientation == "vertical")
    return "row"
}

export const Container = styled.div<IContainerProps>`
  display: flex;
  flex-direction: ${({ orientation }) => getContainerDirection(orientation)};
  height: 100%;
  .MuiTabs-indicator {
    display: none;
  }
`

export const TabContent = styled.div`
  height: 100%;
  width: 100%;
  background-color: #355F55;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 -8px 16px 4px #0000003F;
  z-index: 2;
`

export const CustomTab = styled(Tab)`
  &.MuiTab-root {
    background-color: #5B867C;
    border-radius: 8px 8px 0 0;
    margin-left: 2px;
    max-width: 256px;

    display: flex;
    white-space: nowrap;
    /* overflow: hidden; */
    overflow: hidden;
    text-align: start;
    align-items: flex-start;

    ::after {
      content: ''; /* Create pseudo-element */
      position: absolute;
      right: 0;
      width: 16px;
      height: 100%;
      background: linear-gradient(to left, #5B867C 32%, #0000 100%);
    }

    :not(.Mui-selected){
      opacity: 86%;
      margin-top: 8px;
    }
    :hover {
      opacity: 100%;
    }
    &.Mui-selected {
      background-color: #355F55;
      color: #fff;
      box-shadow: 0 -8px 16px 4px #0000003F;
      z-index: 3;
    }
  }
`

export const TabLabel = styled.span`
  background-color: red;
`
