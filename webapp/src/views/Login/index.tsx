import { useState, useEffect } from "react"
import type { FormEvent } from "react"

import { TextField } from "@mui/material"
import LoadingButton from '@mui/lab/LoadingButton';

import { validateToken, createNewSession } from "services/sessionServices";
import {
  Container,
  LoginForm,
} from "./styles"


export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const submitLogin = (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)

    createNewSession({ email, password }).then(
      response => response && localStorage.setItem("jwt", response)
    )

    setIsLoading(false)
  }

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    const isValid = validateToken(token)
    if (!isValid)
      return
    //todo do redirect
  }, [])

  return (
    <Container>
      <LoginForm onSubmit={submitLogin}>
        <TextField
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <TextField
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <LoadingButton
          variant="contained"
          loading={isLoading}
        >
          Login
        </LoadingButton>
      </LoginForm>
    </Container>
  )
}
