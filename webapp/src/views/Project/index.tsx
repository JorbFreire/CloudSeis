import { useState, FormEvent } from 'react'
import api from '../../services/api'
import { useNavigate } from '@tanstack/react-location'
import { Container, FileInput, Button } from './styles'

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';
import ButtonMUI from '@mui/material/Button'

interface IProjectProps {
  projectName?: string
}

interface ITreeline {
  id: string
}

export default function Project({ projectName }: IProjectProps) {
  const navigate = useNavigate()
  const [SUFiles, setSUFiles] = useState<FileList | null>()
  const [lastFileName, setLastFileName] = useState("")
  const [loading, setLoading] = useState(false)
  const [treelines, setTreelines] = useState<Array<ITreeline>>([])

  const openDataWindow = () => navigate({ to: `/seismic-visualization/${lastFileName}` })

  const submitFiles = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (SUFiles && !loading) {
      setLoading(true)

      const formData = new FormData();
      formData.append('file', SUFiles[0]);

      try {
        const response = await api.post('/su-file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        setLastFileName(response.data.unique_filename)
      } catch (error) {
        console.error(error)
      }

      setLoading(false)
    }
  }

  const treeView = () => {
    const tempTreelines = treelines
    tempTreelines.push({id: `${Math.random()}`})

    setTreelines([...tempTreelines])
  }

  return (
  
    <Container onSubmit={submitFiles}>

      <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ height: 240, flexGrow: 1, maxWidth: 400, overflowY: 'auto' }}
      >

        <Button onClick={treeView}>
          Create Line
        </Button>

          {treelines.map((treeline) => (
            <TreeItem nodeId={treeline.id} label={`Line ${treeline.id}`}>
              <Button className='workFlowButton'>Create Workflow</Button>
            </TreeItem>
          ))}
        


        <TreeItem nodeId="5" label="Documents">
          <TreeItem nodeId="10" label="OSS" />
          <TreeItem nodeId="6" label="MUI">
            <TreeItem nodeId="8" label="index.js" />
          </TreeItem>
        </TreeItem>
      </TreeView>

      <h1>{projectName}</h1>
      <FileInput
        type="file"
        onChange={(event) => setSUFiles(event.target.files)}
      />

      <Button type='submit'>
        {loading ? 'uploading...' : 'Upload'}
      </Button>

      <Button onClick={openDataWindow}>
        Display Seismic Data
      </Button>
    </Container>
  )
}
