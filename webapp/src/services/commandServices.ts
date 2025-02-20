import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';
import { StaticTabKey } from 'constants/StaticTabKey'

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function createNewCommand(
  token: string,
  workflowId: number,
  program_id: number,
  name: string,
): Promise<ICommand | null> {
  try {
    const response = await api.post<ICommand>(
      `/command/create/${workflowId}`,
      {
        name,
        program_id,
        parameters: "{}"
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

export async function updateCommandParameters(
  token: string,
  // ! id type must be reviewed, StaticTabKey would cause errors
  id: number | StaticTabKey,
  newParameters: string
): Promise<ICommand | null> {
  try {
    const response = await api.put<ICommand>(
      `/command/update/${id}/parameters`,
      {
        parameters: newParameters
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

export async function updateCommandIsActive(
  token: string,
  // ! id type must be reviewed, StaticTabKey would cause errors
  id: number | StaticTabKey,
): Promise<ICommand | null> {
  try {
    const response = await api.put<ICommand>(
      `/command/update/${id}/is_active`,
      {},
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

export async function updateCommandsOrder(
  token: string,
  workflowId: string,
  newOrder: idsType
): Promise<orderedCommandsListType | null> {
  try {
    const response = await api.put<orderedCommandsListType>(
      `/command/order/${workflowId}`,
      { newOrder },
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

export async function deleteCommand(
  token: string,
  commandId: string,
): Promise<ICommand | null> {
  try {
    const response = await api.delete<ICommand>(
      `/command/delete/${commandId}`,
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
