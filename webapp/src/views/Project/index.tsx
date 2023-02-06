import { useState, useEffect } from 'react'
import axios from 'axios'
import { useNavigate } from '@tanstack/react-location'
import { Container, FileInput, StartButton } from './styles'

interface IProjectProps {
  projectName?: string
}

export default function Project({ projectName }: IProjectProps) {
  const navigate = useNavigate()
  const [SUFiles, setSUFiles] = useState<FileList | null>()
  const [readingFile, setReadingFile] = useState(false)


  const openDataWindow = () => navigate({ to: '/seismic-visualization/0' })

  useEffect(() => {
    if (SUFiles && !readingFile) {
      setReadingFile(true)
      try {
        axios.get('https://localhost:3001')
      } catch (error) {

      }
    }
  }, [SUFiles])

  return (
    <Container>
      <h1>{projectName}</h1>
      <FileInput
        type="file"
        onChange={(event) => setSUFiles(event.target.files)}
      />
      <StartButton onClick={openDataWindow}>
        Display Seismic Data
      </StartButton>
    </Container>
  )
}
