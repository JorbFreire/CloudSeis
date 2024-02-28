import type { Dispatch, SetStateAction } from 'react'

import GenericDrawer from "../GenericDrawer"

interface IProgramsDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function ProgramsDrawer({
  isOpen,
  setIsOpen
}: IProgramsDrawerProps) {
  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='right'
    >
      <h1>Programs</h1>
    </GenericDrawer>
  )
}
