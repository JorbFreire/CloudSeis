declare type navigationOrientationType = 'horizontal' | 'vertical'
declare type navigationColorType = "primary" | "secondary" | "white"


declare interface IContainerProps {
  $orientation: navigationOrientationType
}

declare interface ICustomTabContainerProps extends IContainerProps {
  $color: navigationColorType
}

declare interface ICustomTabProps extends ICustomTabContainerProps {
  label: string
  value: number
}

declare interface ITabContentProps extends IContainerProps {
  $color: navigationColorType
}
