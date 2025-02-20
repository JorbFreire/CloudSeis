import styled, { css } from "styled-components";
import Tab from '@mui/material/Tab';
import IconButton from "@mui/material/IconButton";


interface IActionButtonProps {
  $isActive: boolean
}

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
      width: 256px;
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

export const Container = styled.div`
  position: relative;
`

export const TabBody = styled(Tab) <ICustomTabContainerProps>`
  &.MuiTab-root.MuiButtonBase-root {
    display: flex;
    align-items: flex-start;
    white-space: nowrap;
    overflow: hidden;
    max-width: 256px;

    ${({ $orientation }) => getCustumTabOrientationStyles($orientation)}
    ${({ $color }) => getCustomTabColorStyles($color)}
    ${({ $isActive }) => !$isActive && 'font-style: italic; text-decoration-line: line-through; opacity: 87%'}


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

export const ActionButtonsContainer = styled.div`
  position: absolute;
  right: 8px;
  top: 2px;
  z-index: 10;
`

export const ActionButton = styled(IconButton)`
  &.MuiIconButton-root {
    z-index: 10;
    
    height: 44px;
    width: 44px;
  }
`
