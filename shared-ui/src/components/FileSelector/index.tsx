import { useState } from "react"

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from "@mui/material/Button"

import FileUploadDialog from "../FileUploadDialog"
import { uploadNewFileType } from "../FileUploadDialog"

interface IFileSelectorProps {
  label?: string
  fileLinks: Array<IfileLink>
  selectedFileLinkId: string | undefined
  onSubmitFileLinkUpdate: (fileLinkId: string) => void
  uploadNewFile: uploadNewFileType
}

export default function FileSelector({
  label = "Arquivo",
  fileLinks,
  selectedFileLinkId,
  onSubmitFileLinkUpdate,
  uploadNewFile,
}: IFileSelectorProps) {
  const [isFileUploadDialogOpen, setIsFileUploadDialogOpen] = useState<boolean>(false)

  return (
    <>
      <Select
        value={selectedFileLinkId}
        label={label}
        onChange={(event) => onSubmitFileLinkUpdate(event.target.value)}
      >
        {fileLinks.map((fileLink) =>
          <MenuItem key={fileLink.id} value={fileLink.id}>
            {fileLink.name}
          </MenuItem>
        )}

        <Button
          onClick={() => setIsFileUploadDialogOpen(true)}
        >
          Upload de novo arquivo
        </Button>
      </Select>

      <FileUploadDialog
        open={isFileUploadDialogOpen}
        setOpen={setIsFileUploadDialogOpen}
        uploadNewFile={uploadNewFile}
      />
    </>
  )
}
