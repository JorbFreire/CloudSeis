import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function getProjectsByUser(token: string): Promise<Array<IProject> | null> {
  try {
    const response = await api.get<Array<IProject>>(`/project/list`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function createNewProject(token: string, name: string): Promise<IProject | null> {
  try {
    const response = await api.post<IProject>(
      `/project/create`,
      { name },
      {
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function deleteProject(token: string, id: number): Promise<IProject | null> {
  try {
    const response = await api.delete<IProject>(
      `/project/delete/${id}`,
      {
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}
