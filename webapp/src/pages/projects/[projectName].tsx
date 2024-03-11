import { useMatch } from '@tanstack/react-location'
import SelectedWorkflowsProvider from 'providers/SelectedWorkflowsProvider'
import ProjectView from 'views/Project'

export default function ProjectPage() {
  const { params } = useMatch()

  return (
    <SelectedWorkflowsProvider>
      <ProjectView
        projectName={params.projectName}
        projectId={params.projectId}
      />
    </SelectedWorkflowsProvider>
  )
}
