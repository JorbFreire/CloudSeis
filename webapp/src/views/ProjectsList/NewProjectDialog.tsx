import { useState } from 'react';
import type { FormEvent } from 'react';

import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';

import AddRoundedIcon from "@mui/icons-material/AddRounded"

import { createNewProject } from 'services/projectServices';

import { AddProjectButton } from './styles'

interface INewProjectDialogProps {
  pushNewProject(newProject: IProject): void
}

export default function NewProjectDialog({ pushNewProject }: INewProjectDialogProps) {
  const [open, setOpen] = useState(false)
  const [projectName, setProjectName] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const closeDialog = () => {
    setOpen(false)
  }

  const submitNewProject = (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)
    const token = localStorage.getItem("jwt")
    token && createNewProject(token, projectName)
      .then((newProject) => newProject && pushNewProject(newProject))
    setIsLoading(false)
    closeDialog()
  }

  return (
    <>
      <Dialog
        open={open}
        onClose={closeDialog}
        component="form"
        onSubmit={submitNewProject}
      >
        <DialogContent>
          <TextField
            label="Nome do projeto"
            value={projectName}
            onChange={(event) => setProjectName(event.target.value)}
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={closeDialog} >
            Cancelar
          </Button>

          <LoadingButton
            type='submit'
            loading={isLoading}
          >
            Salvar
          </LoadingButton>
        </DialogActions>
      </Dialog>

      <AddProjectButton
        color='primary'
        onClick={() => setOpen(true)}
      >
        <AddRoundedIcon />
      </AddProjectButton>
    </>
  )
}