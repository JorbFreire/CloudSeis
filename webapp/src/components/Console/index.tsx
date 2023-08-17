import { Container } from './styles'

interface IConsoleProps {
  messages: Array<string>
}

export default function Console({ messages }: IConsoleProps) {
  return (
    <Container>
      <h4>
        Console
      </h4>
    </Container>
  )
}
