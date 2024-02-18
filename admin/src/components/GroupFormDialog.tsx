import { useState } from "react"
import type { Dispatch, SetStateAction } from "react"

import Dialog from "@mui/material/Dialog"
import DialogContent from '@mui/material/DialogContent'
import Stack from '@mui/material/Stack';
import TextField from "@mui/material/TextField"
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'

import CloseRoundedIcon from '@mui/icons-material/CloseRounded';

import { useProgramGroups } from "../providers/GroupsProvider"

interface IGroupFormDialog {
  open: boolean
  setOpen: Dispatch< SetStateAction<boolean> >
}

export default function GroupFormDialog({ open, setOpen }: IGroupFormDialog) {
  const { createProgramGroup } = useProgramGroups()

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
      fullWidth
    >
      <DialogContent>
        <IconButton
          onClick={() => setOpen(false)}
          sx={{
            position: "absolute",
            top: "16px",
            right: "16px",
          }}
        >
          <CloseRoundedIcon fontSize="large" color="error" />
        </IconButton>

        <Stack
          component="form"
          onSubmit={(event) => {
            event.preventDefault()
            createProgramGroup({name, description})
          }}
          sx={{ gap: "32px", marginTop: "64px" }}
        >      
          <TextField
            label="Nome do grupo"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <TextField
            label="Descrição do grupo"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />

          <Button
            type="submit"
            variant="contained"
          >
            Salvar Novo Grupo
          </Button>
        </Stack>
      </DialogContent>
    </Dialog>
  )
}
