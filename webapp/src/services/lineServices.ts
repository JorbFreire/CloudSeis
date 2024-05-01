import { AxiosError } from "axios"
import api from "./api"

export async function getLinesByProjectID(
  token: string,
  projectID: string
): Promise<Array<ILine> | number> {
  try {
    const response = await api.get<Array<ILine>>(`/line/list/${projectID}`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    if (axiosError.status)
      return axiosError.status
    return []
  }
}

export async function createNewLine(
  token: string,
  projectId: string,
  name: string
): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(
      `/line/create`,
      {
        projectId,
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
