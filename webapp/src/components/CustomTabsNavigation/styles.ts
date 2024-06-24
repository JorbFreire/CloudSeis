import styled, { css } from "styled-components";

export function getContainerDirection($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return "column"
  if ($orientation == "vertical")
    return "row"
}

export function getContentOrientationStyles($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return css`
      width: 100%;
      border-radius: 8px 8px 0 0;
    `
  if ($orientation == "vertical")
    return css`width: calc( 100% - 256px );`
}

export function getContentColorStyles($color: navigationColorType) {
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

export const Container = styled.div<IContainerProps>`
  display: flex;
  flex-direction: ${({ $orientation }) => getContainerDirection($orientation)};
  height: 100%;
  width: 100%;
  .MuiTabs-indicator {
    display: none;
  }
`

export const TabContent = styled.div<ITabContentProps>`
  z-index: 2;
  height: 100%;
  width: 100%;
  padding: 16px 32px;
  ${({ $orientation }) => getContentOrientationStyles($orientation)}
  ${({ $color }) => getContentColorStyles($color)}
`
