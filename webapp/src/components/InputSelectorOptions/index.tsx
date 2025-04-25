import { useEffect, useState } from "react"
import { useLocation } from "@tanstack/react-location";

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
  const location = useLocation()
  const projectId = Number(location.current.pathname.split('/')[2])

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

    let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
    const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
    if (gatherKeyFromStore)
      vizualizerURL += `gather_key=${gatherKeyFromStore}&`
    window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}&origin=input`, '_blank')
  }

  const submitWorkflowFileLinkUpdate = (fileLinkId: string) => {
    const oldFileLinkId = selectedFileLinkId
    setSelectedFileLinkId(fileLinkId)

    if (!singleSelectedWorkflowId)
      return
    if (!fileLinkId)
      return

    updateWorkflowFileLink(
      singleSelectedWorkflowId,
      Number(fileLinkId)
    ).catch((error) => {
      console.log(error)
      setSelectedFileLinkId(oldFileLinkId)
    })
  }

  useEffect(() => {
    listFiles(projectId).then((result) => {
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
        onChange={(event) => submitWorkflowFileLinkUpdate(event.target.value)}
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
        color="primary"
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
