import { useState, FormEvent } from 'react'
import { useNavigate } from '@tanstack/react-location'

import api from '../../services/api'
import { Container, FileInput, Button } from './styles'
import { useSelectedCommand } from 'providers/SelectedCommandProvider'

interface ISUFileInput {
  projectName: string
}
export default function SUFileInput({ projectName }: ISUFileInput) {
  const navigate = useNavigate()
  const { suFileName, setSuFileName } = useSelectedCommand()

  const [SUFiles, setSUFiles] = useState<FileList | null>()
  const [loading, setLoading] = useState(false)

  const openDataWindow = () => window.open(`http://localhost:5006/visualizer?file_name=${suFileName}`)

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
        setSuFileName(response.data.unique_filename)
      } catch (error) {
        console.error(error)
      }

      setLoading(false)
    }
  }

  return (
    <Container onSubmit={submitFiles}>
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
