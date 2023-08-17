import { useMatch } from '@tanstack/react-location'
import ProjectView from 'views/Project'

export default function ProjectPage() {
  const { params } = useMatch()

  return (
    <ProjectView
      projectName={params.projectName}
      projectId={params.projectId}
    />
  )
}
