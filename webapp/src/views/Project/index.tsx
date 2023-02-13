import { useState, FormEvent } from 'react'
import api from '../../services/api'
import { useNavigate } from '@tanstack/react-location'
import { Container, FileInput, Button } from './styles'

interface IProjectProps {
  projectName?: string
}

export default function Project({ projectName }: IProjectProps) {
  const navigate = useNavigate()
  const [SUFiles, setSUFiles] = useState<FileList | null>()
  const [lastFileName, setLastFileName] = useState("")
  const [loading, setLoading] = useState(false)

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
