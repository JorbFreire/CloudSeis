import type { Dispatch, SetStateAction } from 'react'
import GenericDrawer from "../GenericDrawer"

interface ICommandOptionsDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function CommandOptionsDrawer({
  isOpen,
  setIsOpen
}: ICommandOptionsDrawerProps) {
  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='right'
    >
      <h1>Command</h1>
    </GenericDrawer>
  )
}
