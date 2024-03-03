import { css } from "styled-components";

export type orientationType = 'horizontal' | 'vertical'
export type colorType = "primary" | "secondary" | "white"

export function getContainerDirection($orientation: orientationType) {
  if ($orientation == "horizontal")
    return "column"
  if ($orientation == "vertical")
    return "row"
}

export function getCustumTabOrientationStyles($orientation: orientationType) {
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

export function getContentOrientationStyles($orientation: orientationType) {
  if ($orientation == "horizontal")
    return css`
      width: 100%;
      border-radius: 8px 8px 0 0;
    `
  if ($orientation == "vertical")
    return css`width: calc( 100% - 256px );`
}

export function getCustomTabColorStyles($color: colorType) {
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

export function getContentColorStyles($color: colorType) {
  if ($color == "white")
    return css`
      border-radius: 0;
      border-left: 2px solid #fff;
    `
  return css`
    background-color: #355F55;
    box-shadow: 0 -8px 16px 4px #0000003F;
  `
}
