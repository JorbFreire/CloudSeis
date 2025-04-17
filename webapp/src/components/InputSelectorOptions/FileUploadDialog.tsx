import { useState } from "react"
import { useLocation } from "@tanstack/react-location"
import type { Dispatch, SetStateAction } from "react"

import Dialog from '@mui/material/Dialog'
import DialogTitle from '@mui/material/DialogTitle'
import DialogContent from '@mui/material/DialogContent'
import DialogActions from '@mui/material/DialogActions'
import Button from '@mui/material/Button'

import { createFile } from "services/fileServices"
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'

interface IFileUploadDialogProps {
  open: boolean
  setOpen: Dispatch<SetStateAction<boolean>>
  addFileLink: (newFileLink: IfileLink) => void
}

export default function FileUploadDialog({
  open,
  setOpen,
  addFileLink,
}: IFileUploadDialogProps) {
  const location = useLocation()
  const projectId = Number(location.current.pathname.split('/')[2])

  const singleSelectedWorkflowId = useSelectedWorkflowsStore((state) => state.singleSelectedWorkflowId)
  const [file, setFile] = useState<any>(null)

  const saveNewFile = () => {
    if (!singleSelectedWorkflowId)
      return

    if (!file)
      return

    const formData = new FormData();
    formData.append('file', file);

    createFile(
      projectId,
      formData
    ).then((result) => {
      if (!result) return
      addFileLink(result.fileLink)
      setOpen(false)
    })
  }

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
    >
      <DialogTitle>
        Upload novo arquivo .su
      </DialogTitle>

      <DialogContent>
        <input
          type="file"
          onChange={(event) => event.target.files && setFile(event.target.files[0])}
        />
      </DialogContent>

      <DialogActions>
        <Button
          variant="contained"
          onClick={saveNewFile}
        >
          Salvar Novo Arquivo
        </Button>
      </DialogActions>
    </Dialog>
  )
}
