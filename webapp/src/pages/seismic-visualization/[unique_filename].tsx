import { useMatch } from '@tanstack/react-location'
import SeismicVisualizationView from 'views/SeismicVisualization'

export default function SeismicVisualizationPage() {
  const { params } = useMatch()

  return (
    <SeismicVisualizationView unique_filename={params.unique_filename} />
  )
}
