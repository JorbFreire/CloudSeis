import styled from "styled-components";
import Tab from '@mui/material/Tab';

import type {
  colorType,
  orientationType,
} from "./styleGetters"

import {
  getContainerDirection,
  getCustumTabOrientationStyles,
  getContentOrientationStyles,
  getCustomTabColorStyles,
  getContentColorStyles,
} from './styleGetters'


interface IContainerProps {
  $orientation: orientationType
}

interface ICustomTabProps extends IContainerProps {
  $color: colorType
}
interface ITabContentProps extends IContainerProps {
  $color: colorType
}

export const Container = styled.div<IContainerProps>`
  display: flex;
  flex-direction: ${({ $orientation }) => getContainerDirection($orientation)};
  height: 100%;
  .MuiTabs-indicator {
    display: none;
  }
`

export const TabContent = styled.div<ITabContentProps>`
  z-index: 2;
  height: 100%;
  ${({ $orientation }) => getContentOrientationStyles($orientation)}
  ${({ $color }) => getContentColorStyles($color)}
`

export const CustomTab = styled(Tab) <ICustomTabProps>`
  &.MuiTab-root.MuiButtonBase-root {
    display: flex;
    align-items: flex-start;
    white-space: nowrap;
    overflow: hidden;
    max-width: 256px;    
    
    ${({ $orientation }) => getCustumTabOrientationStyles($orientation)}
    ${({ $color }) => getCustomTabColorStyles($color)}

    .MuiTouchRipple-root {
      z-index: 3;
    }

    ::after {
      content: '';
      position: absolute;
      right: 0;
      width: 32px;
      height: 100%;
    }

    :not(.Mui-selected){
      opacity: 86%;
      :hover {
        opacity: 100%;
      }
    }

    &.Mui-selected {
      cursor: auto;
      z-index: 10;
      box-shadow: 0 -8px 16px 4px #0000003F;
      .MuiTouchRipple-root {
        display: none;
      }
    }
  }
`
