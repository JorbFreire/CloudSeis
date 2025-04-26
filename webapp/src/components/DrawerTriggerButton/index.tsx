import type { ReactNode, Dispatch, SetStateAction } from 'react';

import {
  CustomFab
} from './styles'

import type { IFloatButtonProps } from './styles'

interface IDrawerTriggerButton extends IFloatButtonProps {
  children?: ReactNode
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function DrawerTriggerButton({
  children,
  setIsOpen,
  $top,
  $bottom,
  $left,
  $right,
}: IDrawerTriggerButton) {
  return (
    <CustomFab
      size='small'
      color='secondary'
      onClick={() => setIsOpen(true)}

      $top={$top}
      $bottom={$bottom}
      $left={$left}
      $right={$right}
    >
      {children}
    </CustomFab>
  )
}
