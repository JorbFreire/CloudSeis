import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

interface sessionRequestBody {
  email: string
  password: string
}

interface sessionResponse {
  token: string
}

export async function validateSession(token: string): Promise<boolean> {
  try {
    // ! insecure
    const response = await api.get(`/session/validate/${token}`)
    if (response.status == 200)
      return true
    return false
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return false
  }
}

export async function createNewSession({
  email,
  password
}: sessionRequestBody): Promise<string | null> {
  try {
    const response = await api.post<sessionResponse>(`/session/`, {
      email,
      password
    })
    return response.data.token
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}
