import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function getLinesByProjectID(
  token: string,
  projectId: number
): Promise<Array<ILine> | null> {
  try {
    const response = await api.get<Array<ILine>>(`/line/list/${projectId}`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
    return response.data
  } catch (error) {
    console.error(error);
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function createNewLine(
  token: string,
  projectId: number,
  name: string
): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(
      `/line/create/${projectId}`,
      {
        name
      },
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
