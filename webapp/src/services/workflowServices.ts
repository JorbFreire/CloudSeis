import { AxiosError } from "axios"
import api from "./api"

export async function getWorkflowByID(
  token: string,
  id: number,
): Promise<IWorkflow | null | 401> {
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
    if (axiosError.status === 401)
      return 401
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
    return null
  }
}
