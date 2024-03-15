import { useState } from "react"

import IconButton from "@mui/material/IconButton"
import Button from "@mui/material/Button"
import DeleteForeverRoundedIcon from '@mui/icons-material/DeleteForeverRounded';

interface IDeleteButtonProps {
  onClick(): void
  size?: "small" | "medium" | "large"
}

export default function DeleteButton({
  onClick,
  size="large"
}: IDeleteButtonProps) {
  const [allowDelete, setAllowDelete] = useState(false)

  const displayDeleteButton = () => {
    setAllowDelete(true)
    setTimeout(() => {
      setAllowDelete(false)
    }, 4000);
  }

  return (
    <IconButton
      onClick={displayDeleteButton}
      color="error"
    >
      <Button
        onClick={onClick}
        variant="contained"
        color="error"
        sx={{
          position: "absolute",
          right: 0,
          display: allowDelete ? "flex" : "none"
        }}
      >
        Deletar
      </Button>
      <DeleteForeverRoundedIcon color="error" fontSize={size} />
    </IconButton>
  )
}
