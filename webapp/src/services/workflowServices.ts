import { AxiosError } from "axios"

import useNotificationStore from 'store/notificationStore';
import { defaultOutputName } from 'constants/defaults'


import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function getWorkflowByID(
  token: string,
  id: number,
): Promise<IWorkflow | null> {
  try {
    const response = await api.get<IWorkflow>(
      `/workflow/show/${id}`,
      {
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
    )
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

export async function createNewWorkflow(
  token: string,
  parentId: number,
  parentType: "projectId" | "lineId",
  name: string,
): Promise<IResumedWorkflow | null> {
  try {
    const response = await api.post<IResumedWorkflow>(
      `/workflow/create/${parentId}`,
      {
        parentType,
        name,
        output_name: defaultOutputName
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

export async function updateWorkflowFileLink(
  token: string,
  workflowId: number,
  fileLinkId: number,
): Promise<IWorkflow | null> {
  try {
    const response = await api.put<IWorkflow>(
      `/workflow/update/${workflowId}/file`,
      {
        fileLinkId
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

export async function updateWorkflowOutputName(
  token: string,
  workflowId: number,
  outputName: string,
): Promise<IWorkflow | null> {
  try {
    const response = await api.put<IWorkflow>(
      `/workflow/update/${workflowId}/output-name`,
      {
        outputName
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
