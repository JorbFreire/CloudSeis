import { Container } from './styles'

interface IProjectsListProps {
  projectKey: string
}

export default function ProjectsList({ projectKey }: IProjectsListProps) {
  return (
    <Container>
      <h1>{projectKey}</h1>
    </Container>
  )
}
