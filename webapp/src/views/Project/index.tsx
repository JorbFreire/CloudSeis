import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from '@tanstack/react-location'
import { Container, FileInput, StartButton } from './styles'

interface IProjectProps {
  projectName?: string
}

export default function Project({ projectName }: IProjectProps) {
  const navigate = useNavigate()
  const [SUFiles, setSUFiles] = useState<FileList | null>()
  const [SUFileInBase64, setSUFileInBase64] = useState<string>()
  const [readingFile, setReadingFile] = useState(false)

  const getBase64 = (file: File) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onload = () => {
      console.log('file reader load finished')
      if (typeof reader.result == 'string')
        return console.error(`result on file reading came with type: ${typeof reader.result}`)

      // Converting to String to String becouse of a typescript error.
      const base64String = String(reader.result)
        .replace('data:', '')
        .replace(/^.+,/, '');
      setSUFileInBase64(base64String)
      setReadingFile(false)
    };
    reader.onerror = (error) => {
      console.error('Error: ', error);
      setReadingFile(false)
    };
  }

  const getBase64CallBack = useCallback(getBase64, [setSUFileInBase64, setReadingFile])

  const openDataWindow = () => navigate({ to: '/seismic-visualization/0' })

  useEffect(() => {
    if (SUFiles && !readingFile) {
      setReadingFile(true)
      getBase64CallBack(SUFiles[0])
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
