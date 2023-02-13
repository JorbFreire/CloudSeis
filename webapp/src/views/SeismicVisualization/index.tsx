import { useState, useEffect } from "react"
import api from '../../services/api'
import { Container } from "./styles"

interface SeismicVisualizationProps {
  fileKey: string
}

export default function SeismicVisualization({ fileKey }: SeismicVisualizationProps) {
  const [plotDiv, setPlotDiv] = useState("")
  const [plotScript, setPlotScript] = useState("")

  useEffect(() => {
    const getPlotHTML = async () => {
      try {
        const response = await api.get('/get-plot')
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
      <h1>Key: {fileKey}</h1>
      <div dangerouslySetInnerHTML={{ __html: plotDiv }} />
    </Container>
  )
}
