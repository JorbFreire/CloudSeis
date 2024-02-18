import IconButton from "@mui/material/IconButton"

interface IDeleteButtonProps {
  onClick(): void
}

export default function DeleteButton({ onClick }: IDeleteButtonProps) {
  return (
    <IconButton onClick={onClick}>
      D
    </IconButton>
  )
}
