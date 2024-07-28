import { useEffect, useState } from "react"

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import Button from "@mui/material/Button"

import { listFiles, createFile } from "services/fileServices"
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'

import { Container } from "./styles"

interface IfileLink {
  id: number
  name: string
  data_type: string
  projectId: number
}

export default function InputSelectorOptions() {
  const singleSelectedWorkflowId = useSelectedWorkflowsStore((state) => state.singleSelectedWorkflowId)

  const [fileLinks, setFileLinks] = useState<Array<IfileLink>>([])
  const [selectedFileLink, setSelectedFileLink] = useState<string | undefined>()

  const [file, setFile] = useState<any>(null)

  const saveNewFile = () => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    if (!singleSelectedWorkflowId)
      return

    if (!file)
      return

    const formData = new FormData();
    formData.append('file', file);

    //! projectId is mocked
    createFile(token, 1, formData).then((result) => {
      console.log("file created")
    })
  }

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    //! projectId is mocked
    listFiles(token, 1).then((result) => {
      if (!result)
        return
      console.log("result")
      console.log(result)
      setFileLinks(result)
    })
  }, [])

  return (
    <Container>
      <h1>Escolha o arquivo .su</h1>
      <input
        type="file"
        onChange={(event) => event.target.files && setFile(event.target.files[0])}
      />

      <Select
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={selectedFileLink}
        label="Arquivo"
        onChange={(event) => setSelectedFileLink(event.target.value)}
      >
        {fileLinks.map((fileLink) =>
          <MenuItem value={fileLink.id}>
            {fileLink.name}
          </MenuItem>
        )}
      </Select>

      <Button
        variant="contained"
        onClick={saveNewFile}
      >
        Salvar Novo Arquivo
      </Button>
    </Container>
  )
}
