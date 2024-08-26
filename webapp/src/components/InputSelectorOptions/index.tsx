import { useEffect, useState } from "react"

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from "@mui/material/Button"

import { listFiles } from "services/fileServices"
import { updateWorkflowFileLink } from "services/workflowServices";
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { useGatherKeyStore } from 'store/gatherKeyStore'

import FileUploadDialog from "./FileUploadDialog"
import { Container } from "./styles"

export default function InputSelectorOptions() {
  const {
    selectedWorkflows,
    singleSelectedWorkflowId,
  } = useSelectedWorkflowsStore((state) => ({
    selectedWorkflows: state.selectedWorkflows,
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
  }))
  const gatherKeys = useGatherKeyStore((state) => state.gatherKeys)

  const [fileLinks, setFileLinks] = useState<Array<IfileLink>>([])
  const [selectedFileLinkId, setSelectedFileLinkId] = useState<string | undefined>("0")

  const [isFileUploadDialogOpen, setIsFileUploadDialogOpen] = useState<boolean>(false)

  const addFileLink = (newFileLink: IfileLink) => {
    setFileLinks([...fileLinks, newFileLink])
    setSelectedFileLinkId(newFileLink.id.toString())
  }

  const visualizeInputFile = () => {
    if (!singleSelectedWorkflowId) return

    let vizualizerURL = `${import.meta.env.VITE_API_URL}/?`
    const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
    if (gatherKeyFromStore)
      vizualizerURL += `gather_key=${gatherKeyFromStore}&`
    window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}&origin=input`, '_blank')
  }

  const submitWorkflowFileLinkUpdate = () => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    if (!singleSelectedWorkflowId)
      return
    if (!selectedFileLinkId)
      return

    updateWorkflowFileLink(
      token,
      singleSelectedWorkflowId,
      Number(selectedFileLinkId)
    )
  }

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    //! projectId is mocked
    listFiles(token, 1).then((result) => {
      if (!result)
        return
      setFileLinks(result)

      const a = selectedWorkflows.filter(
        (workflow) => workflow.id == singleSelectedWorkflowId
      )
      const fileLinkId = a[0].file_link_id
      setSelectedFileLinkId(fileLinkId.toString())
    })
  }, [])

  return (
    <Container>
      <h1>Escolha o arquivo .su a ser usado no fluxo</h1>

      <Select
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={selectedFileLinkId}
        label="Arquivo"
        onChange={(event) => setSelectedFileLinkId(event.target.value)}
      >
        {fileLinks.map((fileLink) =>
          <MenuItem value={fileLink.id}>
            {fileLink.name}
          </MenuItem>
        )}

        <Button
          onClick={() => setIsFileUploadDialogOpen(true)}
        >
          Upload de novo arquivo
        </Button>
      </Select>

      <Button
        variant="contained"
        onClick={submitWorkflowFileLinkUpdate}
      >
        Alterar arquivo
      </Button>

      <Button
        variant="contained"
        color="secondary"
        onClick={visualizeInputFile}
      >
        Visualizar input
      </Button>

      <FileUploadDialog
        open={isFileUploadDialogOpen}
        setOpen={setIsFileUploadDialogOpen}
        addFileLink={addFileLink}
      />
    </Container>
  )
}
