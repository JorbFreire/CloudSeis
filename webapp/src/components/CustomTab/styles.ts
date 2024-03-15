import styled, { css } from "styled-components";
import Tab from '@mui/material/Tab';

export function getCustumTabOrientationStyles($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return css`
      border-radius: 8px 8px 0 0;
      margin-left: 2px;
      :not(.Mui-selected){
        margin-top: 8px;
      }
    `
  if ($orientation == "vertical")
    return css`
      border-radius: 8px 0 0 8px;
      margin-bottom: 8px;
    `
}

export function getCustomTabColorStyles($color: navigationColorType) {
  if ($color == "white")
    return css`
      background-color: #ABABAB;
      color: #355F55;
      ::after {
        background: linear-gradient(to left, #ABABAB 32%, #0000 100%);
      }
      &.Mui-selected {
        background-color: #fff;
        ::after {
          background: linear-gradient(to left, #fff 32%, #0000 100%);
        }
      }
    `
  return css`
    background-color: #5B867C;
    ::after {
      background: linear-gradient(to left, #5B867C 32%, #0000 100%);
    }
    &.Mui-selected {
      color: #fff;
      background-color: #355F55;
      ::after {
        background: linear-gradient(to left, #355F55 32%, #0000 100%);
      }
    }
  `
}

export const Container = styled(Tab) <ICustomTabContainerProps>`
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
