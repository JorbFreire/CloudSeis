import { useState, useEffect } from "react"
import type { FormEvent } from "react"
import { useNavigate } from "@tanstack/react-location"

import { TextField } from "@mui/material"
import LoadingButton from '@mui/lab/LoadingButton';

import { validateToken, createNewSession } from "services/sessionServices";
import {
  Container,
  LoginForm,
  LinksBox,
  Link
} from "./styles"


export default function Login() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const submitLogin = (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)

    createNewSession({ email, password }).then(
      response => response && localStorage.setItem("jwt", response)
    )

    navigate({ to: "/projects" })
    setIsLoading(false)
  }

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    const isValid = validateToken(token)
    if (!isValid)
      return
    navigate({ to: "/projects" })
  }, [])

  return (
    <Container>
      <LoginForm onSubmit={submitLogin}>
        <TextField
          type="email"
          label="E-mail"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <TextField
          type="password"
          label="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <LoadingButton
          type="submit"
          variant="contained"
          loading={isLoading}
        >
          Login
        </LoadingButton>

        <LinksBox>
          <Link to="/account-recovery">
            Esqueci minha senha
          </Link>
          <Link to="/request-access">
            Solicitar acesso
          </Link>
        </LinksBox>
      </LoginForm>
    </Container>
  )
}
