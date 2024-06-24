import { useMatch } from '@tanstack/react-location'
import SelectedWorkflowsProvider from 'providers/SelectedWorkflowsProvider'
import CommandsProvider from 'providers/CommandsProvider'
import SelectedCommandProvider from 'providers/SelectedCommandProvider'
import ProjectView from 'views/Project'

export default function ProjectPage() {
  const { params } = useMatch()

  return (
    <SelectedWorkflowsProvider>
      <CommandsProvider>
        <SelectedCommandProvider>
          <ProjectView
            projectId={Number(params.projectId)}
          />
        </SelectedCommandProvider >
      </CommandsProvider>
    </SelectedWorkflowsProvider>
  )
}
