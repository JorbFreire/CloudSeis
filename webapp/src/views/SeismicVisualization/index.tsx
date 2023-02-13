import { useState, useEffect } from "react"
import api from '../../services/api'
import { Container } from "./styles"

interface SeismicVisualizationProps {
  unique_filename: string
}

export default function SeismicVisualization({ unique_filename }: SeismicVisualizationProps) {
  const [plotDiv, setPlotDiv] = useState("")
  const [plotScript, setPlotScript] = useState("")

  useEffect(() => {
    const getPlotHTML = async () => {
      try {
        const response = await api.get(`/get-plot/${unique_filename}`)
        setPlotDiv(response.data.div)
        setPlotScript(response.data.script)
      } catch (error) {
        console.error(error)
      }
    }
    getPlotHTML()
  }, [])

  useEffect(() => {
    const plotScriptContent = plotScript
      .replace('<script type="text/javascript">', '')
      .replace('</script>', '')
    new Function(plotScriptContent)()
  }, [plotDiv])

  return (
    <Container>
      <h1>File name: {unique_filename}</h1>
      <div dangerouslySetInnerHTML={{ __html: plotDiv }} />
    </Container>
  )
}
