declare type navigationOrientationType = 'horizontal' | 'vertical'
declare type navigationColorType = "primary" | "secondary" | "white"

declare type onRemoveActionType = (itemId: number) => void

declare interface IContainerProps {
  $orientation: navigationOrientationType
}

declare interface ICustomTabContainerProps extends IContainerProps {
  $color: navigationColorType
}


declare interface ICustomTabProps extends ICustomTabContainerProps {
  label: string
  value: number
  onRemove(): void
}

declare interface ITabContentProps extends IContainerProps {
  $color: navigationColorType
}
